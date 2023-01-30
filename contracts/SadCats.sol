// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "./ERC721A.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "./Delegates.sol";

contract SadCatsNFT is ERC721A, ReentrancyGuard, Delegated {
    using Strings for uint256;
    mapping(address => uint256) private _balances;

    // ======== SUPPLY ========
    uint256 public constant MAX_SUPPLY = 7;

    // ======== PRICE ========
    uint256 public allowListPrice = 0.1 ether;
    uint256 public publicSalePrice = 0.12 ether;

    // ======== SALE STATUS ========
    uint8 public currentMintBatch = 0; // 0: Team; 1: Whitelisted; 2: Public

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

    function whitelistMint(bytes32[] calldata _proof)
        external
        payable
        callerIsUser
    {
        require(currentMintBatch == 1, "Incorrect mint batch");
        require(msg.value == publicSalePrice, "Incorrect ether sent");
        require(totalSupply() < MAX_SUPPLY, "Max supply reached");
        require(_numberMinted(msg.sender) < 1, "Already minted");
        require(
            MerkleProof.verify(
                _proof,
                mintBatch2Root,
                keccak256(abi.encodePacked(msg.sender))
            ),
            "Invalid proof"
        );
        _safeMint(msg.sender, 1);
    }

    // public mint - allow users to mint 1 NFT
    function publicMint() external payable callerIsUser {
        require(currentMintBatch == 3, "Incorrect mint batch");
        require(totalSupply() < MAX_SUPPLY, "Max supply reached");
        require(_numberMinted(msg.sender) < 1, "Already minted");
        require(msg.value == publicSalePrice, "Incorrect ether sent");
        _safeMint(msg.sender, 1);
    }

    function teamMint(uint256 _quantity) external onlyOwner {
        require(totalSupply() + _quantity <= MAX_SUPPLY, "Max supply reached");
        _safeMint(msg.sender, _quantity);
    }

    // ========= GETTERS ===========
    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        override
        returns (string memory)
    {
        require(
            _exists(tokenId),
            "ERC721aMetadata: URI query for nonexistent token"
        );

        if (!isRevealed) {
            return notRevealedURI;
        }

        return
            string(
                abi.encodePacked(
                    _baseTokenURI,
                    tokenId.toString(),
                    baseExtension
                )
            );
    }

    function _startTokenId()
        internal
        view
        virtual
        override(ERC721A)
        returns (uint256)
    {
        return 1;
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

    function setBaseURI(string calldata baseURI) external onlyDelegates {
        _baseTokenURI = baseURI;
    }

    function setNotRevealedURI(string memory _notRevealedURI)
        public
        onlyDelegates
    {
        notRevealedURI = _notRevealedURI;
    }

    function setIsRevealed(bool _reveal) external onlyDelegates {
        isRevealed = _reveal;
    }

    // ======== WITHDRAW ========

    function withdraw(uint256 amount_) external onlyOwner {
        require(
            address(this).balance >= amount_,
            "Address: insufficient balance"
        );

        // This will payout the owner 100% of the contract balance.
        // Do not remove this otherwise you will not be able to withdraw the funds.
        // =============================================================================
        (bool os, ) = payable(owner()).call{value: amount_}("");
        require(os);
        // =============================================================================
    }
    
    modifier callerIsUser() {
        require(tx.origin == msg.sender, "The caller is another contract");
        _;
    }
}