import { app } from "./app.config";
import { Logger } from "./common/logger";
import { connectWithMongoDB } from "./config/mongo.connection"
import { settings } from "./config/settings";


// App Logger
const APP_LOGGER = new Logger("APPLICATION")

/**
 * Utility helper to start the server. This helper will initialize all the 
 * services before starting the server and finally, informs if there is any
 * error starting the server.
 * 
 * @author amanfoundongithub
 */
const startServer = async () => {
    try {
        await connectWithMongoDB();
        
        APP_LOGGER.info("Connected. Now starting the server...")

        app.listen(settings.PORT, () => {
            APP_LOGGER.info(`Success! The service is now live on the port ${settings.PORT}`)
        })

    } catch(e) {
        APP_LOGGER.error(`Error in connection. Server closed.`)
    }  
}

startServer();