import { settings } from "../config/settings.js";
import { Colors } from "./constants.js";

export class Logger {
    name: string;
    debugMode: boolean;

    constructor(name: string) {
        this.name = name;
        this.debugMode = settings.DEBUG_MODE;
    }

    info = (message: any) => {
        console.log(`${this.getPrefix('INFO', Colors.GREEN)} ${this.formatMessage(message)}`);
    }

    error = (message: any) => {
        console.log(`${this.getPrefix('ERROR', Colors.RED)} ${this.formatMessage(message)}`);
    }

    warn = (message: any) => {
        console.log(`${this.getPrefix('WARN', Colors.YELLOW)} ${this.formatMessage(message)}`);
    }

    debug = (message: any) => {
        if (this.debugMode) {
            console.log(`${this.getPrefix('DEBUG', Colors.CYAN)} ${this.formatMessage(message)}`);
        }
    }

    private getPrefix(level: string, color: string): string {
        const timestamp = new Date().toISOString().split('T')[1]?.split('Z')[0]; // HH:mm:ss.ms
        const fixedName = this.name.padEnd(20, ' '); 
        const fixedLevel = level.padEnd(7, ' ');    
        
        return `${Colors.DIM}${timestamp}${Colors.RESET} ${color}${fixedLevel}${Colors.RESET} ${Colors.MAGENTA}[${fixedName}]${Colors.RESET}`;
    }

    private formatMessage(message: any): string {
        return typeof message === 'object' 
            ? `\n${JSON.stringify(message, null, 2)}` 
            : message;
    }

}