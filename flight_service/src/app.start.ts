import { app } from "./app.config";
import { Logger } from "./common/logger";
import { connectWithMongoDB } from "./config/mongo.connection"
import { env } from "./config/env.load";

// App Logger
const APP_LOGGER = new Logger("APPLICATION")

const startServer =  () => {

    connectWithMongoDB().then(() => {
        APP_LOGGER.info("Connected. Now starting the server...")
        app.listen(env.PORT, () => {
            APP_LOGGER.info(`Success! The service is now live on the port ${env.PORT}`)
        })
    })
        .catch((err) => {
            throw new Error(err)
        })
}

startServer()