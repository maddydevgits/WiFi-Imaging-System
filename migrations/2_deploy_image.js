const image=artifacts.require('image');

module.exports=function(deployer){
    deployer.deploy(image);
}