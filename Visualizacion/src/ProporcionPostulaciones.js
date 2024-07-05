const width_map = 1800
const height_map = 800


radius_max = 15

d3.select("#Title").text("Postulaciones y Vacantes tienen escalas separadas")

d3.select("#representando").text("Postulaciones")

const map = d3.select("#map").append("svg")
    .attr("width", width_map)
    .attr("height", height_map)
    .style("background-color", "#f0f0f0")
    .style("border", "1px solid black")
    .style("border-radius", "10px");

const paths = map.append("g")
    .attr("id", "paths")
const hexagonos = map.append("g")
    .attr("id", "hexagonos")


// Define zoom behavior
const zoom = d3.zoom()
    .scaleExtent([0.8, 50]) // Limita el nivel de zoom (mínimo 1x y máximo 10x)
    .on("zoom", (event) => {
        paths.attr("transform", event.transform);
        hexagonos.attr("transform", event.transform);
    });

// Apply zoom behavior to the SVG
map.call(zoom);


d3.json("../data/comunas_ps.geojson").then(joinComunas)
d3.csv("../data/informacion_establecimientos.csv", d3.autoType).then(joinEstablecimientos)



function joinComunas(datos) {
    const menor_densidad = d3.min(datos.features, (d) => d.properties.n_postulaciones / d.properties.vacantes);
    const mayor_densidad = d3.max(datos.features, (d) => d.properties.n_postulaciones / d.properties.vacantes);

    
    const enter = (enter) => {

        const g = enter.append("g")
            .attr("class", "comuna")

        g.append("path")
            .attr("d", caminosGeo)
            .attr("fill", "white")
            .attr("stroke", "black")
            .attr("stroke-width", 1)
            .attr("z-index", 1)
    }

    const update = (update) => {
    }

    const exit = (exit) => {
    }

    const proyeccion = d3.geoMercator()
        .fitSize([width_map, height_map-20], datos);
    
    const caminosGeo = d3.geoPath().projection(proyeccion);

    paths.selectAll(".comuna")
        .data(datos.features, d => d.properties.COMUNA)
        .join(enter, update, exit);       
    
        
    paths.selectAll(".comuna")
        .on("click", (evento, d) => {
        console.log(d.properties.COMUNA)
        console.log(d.properties)
    })
}

function joinEstablecimientos(datos) {
    d3.json("../data/comunas_ps.geojson").then(geo => {

        const proyeccion = d3.geoMercator()
            .fitSize([width_map, height_map-20], geo);

        const hexbin = d3.hexbin()
            .extent([[0, 0], [width_map, height_map-20]])
            .radius(radius_max)
            .x(d => proyeccion([d.LONGITUD, d.LATITUD])[0])
            .y(d => proyeccion([d.LONGITUD, d.LATITUD])[1])
        
        const bins = hexbin(datos);

        const menor_cantidad_postulaciones = d3.min(bins, (d) => d3.sum(d, (e) => e.n_postulaciones));
        const mayor_cantidad_postulaciones = d3.sum(bins, (d) => d3.sum(d, (e) => e.n_postulaciones))/90;
        
        const escalaColoracionDensidad = d3
            .scaleSequential()
            .interpolator(d3.interpolate('white', 'steelblue'))
            .domain([menor_cantidad_postulaciones, mayor_cantidad_postulaciones]);
        

        const enter = (enter) => {

            enter.append("path")
                .attr("d", hexbin.hexagon())
                .attr("transform", d => `translate(${d.x}, ${d.y})`)
                .attr("fill", d => escalaColoracionDensidad(d3.sum(d, (e) => e.n_postulaciones)))
                .attr("z-index", 2)
                .attr("opacity", 0.7)
            enter.append("path")
                .attr("d", hexbin.hexagon())
                .attr("transform", d => `translate(${d.x}, ${d.y})`)
                .attr("stroke", "black")
                .attr("fill", "none")
                .attr("stroke-width", 0.01)
        }           

        const update = (update) => {
        }

        const exit = (exit) => {
        }
        
        hexagonos.selectAll("path")
            .data(bins, d => d.x + ":" + d.y)
            .join(enter, update, exit);        
    })
}