### Sad Cats
View my sad cats on OpenSea right now!!!
```
https://testnets.opensea.io/collection/sad-cats-beta
```

## How to use the scripts
```
brownie compile
brownie run scripts/01_create_metadata.py --network goerli

// make sure you properly set the metadata for the collection.
brownie run scripts/02_deploy.py --network goerli
brownie run scripts/03_create.py --network goerli
```