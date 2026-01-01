export const convertToNumber = (number : string) : number => {
    const val = Number(number)
    if(Number.isNaN(val)) {
        throw new TypeError(`Error during conversion: ${number} is not a valid number.`)
    }
    return val
}