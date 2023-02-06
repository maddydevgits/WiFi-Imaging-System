// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract register {
  
  address[] _users;
  uint[] _passwords;

  mapping(address=>bool) users;

  function registerUser(address username,uint password) public {
    require(!users[username]);

    _users.push(username);
    _passwords.push(password);
  }

  function viewUsers() public view returns(address[] memory,uint[] memory) {
    return(_users,_passwords);
  }

  function loginUser(address username,uint password) public view returns(bool){
    uint i;

    for(i=0;i<_users.length;i++) {
      if(_users[i]==username && _passwords[i]==password) {
        return true;
      }
    }
    return false;
  }
}
