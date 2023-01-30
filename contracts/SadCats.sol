// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "./ERC721A.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "./Delegates.sol";

contract SadCatsNFT is ERC721A, ReentrancyGuard, Ownable {
    using Strings for uint256;
    mapping(address => uint256) private _balances;

    // ======== SUPPLY ========
    uint256 public constant MAX_SUPPLY = 7;

    // ======== PRICE ========
    uint256 public allowListPrice = 0.1 ether;
    uint256 public publicSalePrice = 0.12 ether;

    // ======== SALE STATUS ========
    uint8 public currentMintBatch; // 0: Team; 1: Whitelisted; 2: Public

    // ======== METADATA ========
    bool public isRevealed = false;
    string private _baseTokenURI;
    string private notRevealedURI;
    string private baseExtension = ".json";

    // ======== MERKLE ROOT ========
    bytes32 public mintBatch1Root;
    bytes32 public mintBatch2Root;

    // ======== CONSTRUCTOR ========
    constructor() ERC721A("Sad Cats NFT", "SADCATS") {}

    function publicMint() external payable callerIsUser {
        require(currentMintBatch == 3, "Incorrect mint batch");
        require(totalSupply() < MAX_SUPPLY, "Max supply reached");
        require(_numberMinted(msg.sender) < 1, "Already minted");
        require(msg.value == publicSalePrice, "Incorrect ether sent");
        _safeMint(msg.sender, 1);
    }

    // ======== SETTERS ========
    function setCurrentMintBatch(uint8 _batch) external onlyOwner {
        currentMintBatch = _batch;
    }

    function setAllowListPrice(uint256 _price) external onlyOwner {
        allowListPrice = _price;
    }

    function setPublicSalePrice(uint256 _price) external onlyOwner {
        publicSalePrice = _price;
    }

    function setMintBatch1Root(bytes32 _merkleRoot) external onlyOwner {
        mintBatch1Root = _merkleRoot;
    }

    function setMintBatch2Root(bytes32 _merkleRoot) external onlyOwner {
        mintBatch2Root = _merkleRoot;
    }

    // currently not in use.
    // ensure the caller is a user, not a bot.
    modifier callerIsUser() {
        require(tx.origin == msg.sender, "The caller is another contract");
        _;
    }
}