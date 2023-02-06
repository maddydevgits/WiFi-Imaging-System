// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract image {
  address[] _users;
  string[] _images;
  string[] _names;
  address[][] _tokens;

  mapping(string=>bool) imgs;

  function addImage(address user,string memory name,string memory imageT) public {
    require(!imgs[imageT]);

    imgs[imageT]=true;
    _users.push(user);
    _names.push(name);
    _images.push(imageT);
    _tokens.push([user]);
  }

  function viewImages() public view returns(address[] memory,string[] memory,string[] memory,address[][] memory){
    return(_users,_names,_images,_tokens);
  }

  function addToken(string memory img,address user) public {
    uint i;
    
    for(i=0;i<_images.length;i++){
        if(keccak256(abi.encodePacked(img)) == keccak256(abi.encodePacked(_images[i]))){
            _tokens[i].push(user);
        }
    }
  }

  function removeToken(string memory img,address user) public {
    uint i;
    uint j;

    for(i=0;i<_images.length;i++){
        if(keccak256(abi.encodePacked(img)) == keccak256(abi.encodePacked(_images[i]))){
            for(j=0;j<_tokens[i].length;j++){
                if(_tokens[i][j]==user){
                    delete _tokens[i][j];
                }
            }
        }
    }
  }
}
