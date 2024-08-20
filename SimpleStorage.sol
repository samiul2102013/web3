//SPDX-License-Identifier:MIT
pragma solidity ^0.6.0;

contract SimpleStorage {

    uint256 favoriteNumber;

    struct People{
        string personName ;
        uint256 favoriteNumber;
    }

    People[] public person;
    mapping(string=> uint256)public nameToFavNumber;

    function store(uint256 fav) public {
         favoriteNumber = fav;
    }

    function addpeople(string memory name, uint256 fav) public {
        person.push(People({personName: name, favoriteNumber: fav}));
        nameToFavNumber[name] = fav;
    }

    function retrive() public view returns(uint256) {
        return favoriteNumber;
    }
}