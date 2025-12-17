import { settings } from "../config/settings";
import { Colors } from "./constants";

export class Logger {

    name : string;
    debugMode : boolean;

    constructor(name : string) {
        this.name = name;
        this.debugMode = settings.DEBUG_MODE;
    }

    info = (message : string) => {
        console.log(`${Colors.GREEN}(${this.name})[INFO]\t\t${message}${Colors.RESET}`)
    } 

    error = (message : string) => {
        console.log(`${Colors.RED}(${this.name})[ERROR]\t\t${message}${Colors.RESET}`)
    }

    warn = (message : string) => {
        console.log(`${Colors.YELLOW}(${this.name})[ERROR]\t\t${message}${Colors.RESET}`)
    }

    debug = (message : string) => {
        if(this.debugMode) {
            console.log(`${Colors.CYAN}(${this.name})[DEBUG]\t\t${message}${Colors.RESET}`)
        }
    }

}