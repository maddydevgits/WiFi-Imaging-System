// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract image {
  address[] _users;
  bytes32[] _images;
  address[][] _tokens;

  mapping(bytes32=>bool) imgs;

  function addImage(address user,bytes32 imageT) public {
    require(!imgs[imageT]);

    imgs[imageT]=true;
    _users.push(user);
    _images.push(imageT);
    _tokens.push([user]);
  }

  function viewImages() public view returns(address[] memory,bytes32[] memory,address[][] memory){
    return(_users,_images,_tokens);
  }

  function addToken(bytes32 img,address user) public {
    uint i;
    
    for(i=0;i<_images.length;i++){
        if(_images[i]==img){
            _tokens[i].push(user);
        }
    }
  }
}
