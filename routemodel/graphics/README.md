# Running the UI

The `index.html` file in the `routemodel/graphics` folder contains the code to visualize the map and the datapoints for the path based on a file `data.csv`.

To run it, we need to reach this directory in the terminal:

```bash
cd routemodel/graphics
```

and then run a http.server

```bash
python3 -m http.server
```

This will create a local server where the `index.html` file will be hosted. It can be accessed at `http://localhost:8000`.
