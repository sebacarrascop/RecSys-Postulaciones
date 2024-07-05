const width_map = 1800
const height_map = 800


radius_max = 3

d3.select("#Title").text("Postulaciones y Vacantes tienen escalas separadas")

const map = d3.select("#map").append("svg")
    .attr("width", width_map)
    .attr("height", height_map)
    .style("background-color", "#f0f0f0")
    .style("border", "1px solid black")
    .style("border-radius", "10px");

const paths = map.append("g")
    .attr("id", "paths")
const puntos = map.append("g")
    .attr("id", "puntos")


// Define zoom behavior
const zoom = d3.zoom()
    .scaleExtent([0.8, 50]) // Limita el nivel de zoom (mínimo 1x y máximo 10x)
    .on("zoom", (event) => {
        paths.attr("transform", event.transform);
        puntos.attr("transform", event.transform);
    });

// Apply zoom behavior to the SVG
map.call(zoom);


d3.json("comunas_ps.geojson").then(joinComunas)
d3.csv("recomendaciones_lightfm.csv", d3.autoType).then(joinRecomendaciones)
d3.csv("ubicacion_postulantes.csv", d3.autoType).then(joinPostulantes)




function joinComunas(datos) {
    const enter = (enter) => {

        const g = enter.append("g")
            .attr("class", "comuna")

        g.append("path")
            .attr("d", caminosGeo)
            .attr("stroke", "black")
            .attr("stroke-width", 0.1)
            .attr("fill", "white")
            .attr("z-index", 1)
    }
    const proyeccion = d3.geoMercator()
        .fitSize([width_map, height_map-20], datos);
    
    const caminosGeo = d3.geoPath().projection(proyeccion);

    paths.selectAll(".comuna")
        .data(datos.features, d => d.properties.COMUNA)
        .join(enter);       
    
        
    paths.selectAll(".comuna")
        .on("click", (evento, d) => {
        console.log(d.properties.COMUNA)
        console.log(d.properties)
    })
}

function joinRecomendaciones(datos) {
    d3.json("comunas_ps.geojson").then(datosComunas => {
    const proyeccion = d3.geoMercator()
        .fitSize([width_map, height_map-20], datosComunas);
    const enter = (enter) => {
        const g = enter.append("circle") 
            .attr("class", "establecimiento")
            .attr("transform", d => `translate(${proyeccion([d.lon, d.lat])})`)
            .attr("fill", d => d.color)
            .attr("r", 3)
            .attr("opacity", 1)
    }

    puntos.selectAll(".establecimiento")
        .data(datos)
        .join(enter)
    
    puntos.selectAll(".establecimiento").on("click", (evento, d) => {
            console.log(d.lon, d.lat)
        })
})
}

function joinPostulantes(datos) { 
    d3.json("comunas_ps.geojson").then(datosComunas => {
    const proyeccion = d3.geoMercator()
        .fitSize([width_map, height_map-20], datosComunas);
    const enter = (enter) => {
        const g = enter.append("rect") 
            .attr("class", "postulante")
            .attr("transform", d => `translate(${proyeccion([d.lon, d.lat])})`)
            .attr("fill", d => d.color)
            .attr("width", 3)
            .attr("height", 3)
    }

    puntos.selectAll(".postulante")
        .data(datos)
        .join(enter)
    
    puntos.selectAll(".postulante").on("click", (evento, d) => {
            console.log(d.lon, d.lat)
    })
    })
}