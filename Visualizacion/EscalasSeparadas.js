const width_map = 1800
const height_map = 800

const color_vacantes = "red"
const color_postulaciones = "yellow"

radius_max = 3

d3.select("#Title").text("Postulaciones y Vacantes tienen escalas separadas")


d3.select("#vacantes").style("background-color", color_vacantes)
d3.select("#postulaciones").style("background-color", color_postulaciones)

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


d3.json("comunas_ps.geojson").then(joinComunas)
d3.csv("informacion_establecimientos.csv", d3.autoType).then(joinEstablecimientos)



function joinComunas(datos) {
    const menor_densidad = d3.min(datos.features, (d) => d.properties.n_postulaciones / d.properties.vacantes);
    const mayor_densidad = d3.max(datos.features, (d) => d.properties.n_postulaciones / d.properties.vacantes);

    const escalaColoracionDensidad = d3
        .scaleSequential()
        .interpolator(d3.interpolate('white', 'steelblue'))
        .domain([menor_densidad, mayor_densidad]);
    
    const enter = (enter) => {

        const g = enter.append("g")
            .attr("class", "comuna")

        g.append("path")
            .attr("d", caminosGeo)
            .attr("fill", "white")
            .attr("stroke", "black")
            .attr("stroke-width", 0.1)
            .attr("fill", (d) => escalaColoracionDensidad(d.properties.n_postulaciones / d.properties.vacantes))
            .attr("z-index", 1)

        g.append("text")
            .text(d => Math.round((d.properties.n_postulaciones / d.properties.vacantes)*100)/100)
            .attr("x", d => caminosGeo.centroid(d)[0])
            .attr("y", d => caminosGeo.centroid(d)[1])
            .attr("text-anchor", "middle")
            .attr("dy", 5)
            .attr("fill", "white")
            .attr("font-size", 10)
            .attr("fill", (d) =>((d.properties.n_postulaciones / d.properties.vacantes) < menor_densidad + 0.52*(mayor_densidad-menor_densidad)) ? "black" : "white")
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
    d3.json("comunas_ps.geojson").then(geo => {

        const proyeccion = d3.geoMercator()
            .fitSize([width_map, height_map-20], geo);

        const hexbin = d3.hexbin()
            .extent([[0, 0], [width_map, height_map-20]])
            .radius(radius_max)
            .x(d => proyeccion([d.LONGITUD, d.LATITUD])[0])
            .y(d => proyeccion([d.LONGITUD, d.LATITUD])[1])
        
        const bins = hexbin(datos);

        const menor_cantidad_vacantes = d3.min(bins, (d) => d3.sum(d, (e) => e.vacantes));
        const mayor_cantidad_vacantes = d3.max(bins, (d) => d3.sum(d, (e) => e.vacantes));

        console.log(menor_cantidad_vacantes, mayor_cantidad_vacantes)
        const escalaVacantes = d3
            .scaleLinear()
            .domain([menor_cantidad_vacantes, mayor_cantidad_vacantes])
            .range([0, 1]);

        
        const menor_cantidad_postulaciones = d3.min(bins, (d) => d3.sum(d, (e) => e.n_postulaciones));
        const mayor_cantidad_postulaciones = d3.max(bins, (d) => d3.sum(d, (e) => e.n_postulaciones));

        const escalaPostulaciones = d3
            .scaleLinear()
            .domain([menor_cantidad_postulaciones, mayor_cantidad_postulaciones])
            .range([0, 1]);
        
        

        const enter = (enter) => {

            enter.append("path")
                .attr("d", hexbin.hexagon())
                .attr("transform", d => `translate(${d.x}, ${d.y}), scale(${escalaVacantes(d3.sum(d, (e) => e.vacantes))})`)
                .attr("fill", color_vacantes)
                .attr("z-index", 2)
                .attr("opacity", 0.5)

            enter.append("path")
                .attr("d", hexbin.hexagon())
                .attr("transform", d => `translate(${d.x}, ${d.y}), scale(${escalaPostulaciones(d3.sum(d, (e) => e.n_postulaciones))})`)
                .attr("fill", color_postulaciones)
                .attr("z-index", 1)
                .attr("opacity", 0.5)
            
            
            
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