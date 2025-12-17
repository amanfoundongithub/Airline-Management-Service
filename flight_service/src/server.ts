import express, {Application, Request, Response} from 'express';
import router from './routes/FlightRouter.js';
import { connectWithMongoDB } from './db/client.js';
import { settings } from './config/settings.js';
;


// Initialize an Express Application
const app : Application = express();

app.use(express.json())


app.use('/api/v1/flights', router)

// 3. Simple Health Check
app.get('/', (req: Request, res: Response) => {
    res.send("Flight Service is running...");
});

// 4. Start Database and Server
async function start() {
    await connectWithMongoDB(); 
    app.listen(settings.PORT, () => {
        console.log(`Flight Service listening on http://localhost:${settings.PORT}`);
    });
}

start();