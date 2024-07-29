// Import necessary modules
const { Builder, By, Key } = require('selenium-webdriver');
const readline = require('readline');
const { promisify } = require('util');
const sleep = promisify(setTimeout);

// Configuration variables
const useHeadless = false;
const username = 'YourUsername';
const password = '123456';
const canpin = 'cp01-CP07-15-2';
const zhenpin = 'zp01-ZP07-14-01';

// Terminal colors
const green = '\x1b[32m';
const yellow = '\x1b[33m';
const red = '\x1b[31m';
const reset = '\x1b[0m';

async function resolveLoginPage(driver) {
    // Open the login page
    await driver.get('https://owms-lite-de.cainiao.com/page/cainiao/cnwms/login');

    // Input Username
    const usernameInput = await driver.findElement(By.id('username'));
    await usernameInput.clear();
    await usernameInput.sendKeys(username);
    await sleep(200);

    // Input Password
    const passwordInput = await driver.findElement(By.id('bw'));
    await passwordInput.clear();
    await passwordInput.sendKeys(password);
    await sleep(200);

    // Resolve checkbox
    const checkbox = await driver.findElement(By.id('agree'));
    await checkbox.click();
    await sleep(200);

    // Press Login button
    const buttons = await driver.findElements(By.xpath("//button"));
    await buttons[0].click();
}

function isHNumber(s) {
    // Define the regex pattern
    const pattern = /^H10306600\d{6}01049$/;
    // Match the input string against the pattern
    return pattern.test(s);
}

function sixToH(s) {
    return "H10306600" + s + "01049";
}

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function readInput() {
    return new Promise(resolve => {
        rl.question("Enter Waybill: ", userInput => {
            if (userInput.length === 6) {
                resolve(sixToH(userInput));
            } else if (isHNumber(userInput)) {
                resolve(userInput);
            } else {
                console.log("No Valid Input, try again\n");
                resolve(readInput());
            }
        });
    });
}

async function main() {
    console.log("Version 0.0.1 \n");
    console.log("Alternative Return Interface for Cainiao Warehouse\n");

    // Whether to use headless or normal browser
    const options = new (require('selenium-webdriver/chrome').Options)();
    if (useHeadless) {
        options.headless();
    }

    // Set up the WebDriver
    const driver = new Builder().forBrowser('chrome').setChromeOptions(options).build();

    try {
        // Login with credentials
        await resolveLoginPage(driver);
        console.log("Login Page resolved");

        await sleep(2000);

        // Open return page
        await driver.get("https://owms-lite-de.cainiao.com/page/inbound/receive/cnlReturnReceive?");
        console.log("\nReturn Interface Ready\n");
        await sleep(4000);

        while (true) {
            const inputElement = await driver.findElement(By.xpath("//input[@placeholder='扫描/输入运单号']"));
            const waybillNr = await readInput();
            console.log(waybillNr);

            await sleep(1000);
            await inputElement.clear();
            await inputElement.sendKeys(waybillNr + Key.ENTER);
            await sleep(1000);

            const tdElements = await driver.findElements(By.xpath("//td[@data-next-table-col='0']"));
            const tdElements2 = await driver.findElements(By.xpath("//td[@data-next-table-col='1']"));
            const nrHuopin = tdElements.length;
            let youZheng = false;
            let youCan = false;

            for (let index = 0; index < tdElements.length; index++) {
                let output = "";
                const huopinNr = await tdElements[index].getText();
                output += huopinNr + "\n";
                output += await tdElements2[index].getText() + "\n";

                const huopinElement = await driver.findElement(By.xpath("//input[@placeholder='扫描/输入货品条码']"));
                await huopinElement.clear();
                await huopinElement.sendKeys(huopinNr + Key.ENTER);
                await sleep(300);

                const checkbox = await driver.findElement(By.id('normal'));
                const ariaChecked = await checkbox.getAttribute('aria-checked');

                if (ariaChecked === "false") {
                    await sleep(500);
                    const canzhengElement = await driver.findElement(By.id('cabinetId'));
                    await sleep(500);
                    await canzhengElement.clear();
                    await canzhengElement.sendKeys(canpin);
                    await sleep(200);
                    const body = await driver.findElement(By.xpath("//body"));
                    await sleep(500);
                    youCan = true;
                    output += "Bad Package\n";
                    console.log(yellow + output + reset);
                } else {
                    await sleep(500);
                    const canzhengElement = await driver.findElement(By.id('cabinetId'));
                    await sleep(200);
                    await canzhengElement.clear();
                    await canzhengElement.sendKeys(zhenpin);
                    await sleep(200);
                    const body = await driver.findElement(By.xpath("//body"));
                    await sleep(500);
                    youZheng = true;
                    output += "Good Package\n";
                    console.log(green + output + reset);
                }

                await body.sendKeys(Key.F2);
                await sleep(500);
                await body.sendKeys(Key.F8);
                if (nrHuopin > 1) {
                    await sleep(1000);
                }
            }

            if (youZheng && youCan) {
                console.log(red + "Warning: Mixed Package, open! \n" + reset);
                // playsound('error.mp3');
            }
            if (youZheng && !youCan) {
                console.log(green + "Good Package, throw\n" + reset);
                // playsound('good.mp3');
            }
            if (!youZheng && youCan) {
                console.log(yellow + "Bad Package, throw\n" + reset);
                // playsound('bad.mp3');
            }
        }
    } finally {
        await driver.quit();
    }
}

main();

