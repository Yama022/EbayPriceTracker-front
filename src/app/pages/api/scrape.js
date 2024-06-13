
import { exec } from 'child_process';
import path from 'path';

export default function handler(req, res) {
    if (req.method === 'POST') {
        const { searchQuery } = req.body;
        const scriptPath = path.join(process.cwd(), 'python_scripts', 'scraper.py');
        exec(`python3 ${scriptPath} '${searchQuery}'`, (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                return res.status(500).json({ message: 'Error executing python script', error: stderr });
            }
            try {
                const data = JSON.parse(stdout); // Assurez-vous que votre script Python renvoie des données en JSON
                res.status(200).json(data);
            } catch (err) {
                res.status(500).json({ message: 'Error parsing script output', error: err });
            }
        });
    } else {
        res.setHeader('Allow', ['POST']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}
