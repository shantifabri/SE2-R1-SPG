function cssForHashLoader() {
    const override = `
    margin       : 0;
    position     : absolute;
    top          : 50%;
    left         : 50%;
    -ms-transform: translate(-50%, -50%);
    transform    : translate(-50%, -50%);
  `;
    return override;
}

const hashLoaderSize = 150;

const groupColor = {
    "Softviolet":"color-button-softviolet",
    "Bluegray":"color-button-bluegray",
    "Beige":"color-button-beige",
    "Violetblue":"color-button-violetblue",
    "Violet":"color-button-violet",
    "Greengray":"color-button-greengray",
    "Green":"color-button-green",
    "Red":"color-button-red",
    "Orange":"color-button-orange",
    "Blue":"color-button-blue",
    "Brown":"color-button-brown",
    "Purpleblue":"color-button-purpleblue",
    "Yellow":"color-button-yellow",
    "Lightblue":"color-button-lightblue",
    "Purple":"color-button-purple",
    "Gray":"color-button-gray"
}



const UTILS = { cssForHashLoader, hashLoaderSize, groupColor };
export default UTILS;