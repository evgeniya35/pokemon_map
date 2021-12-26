import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entitiy in PokemonEntity.objects.all():
        add_pokemon(
            folium_map,
            pokemon_entitiy.lat,
            pokemon_entitiy.lon,
            request.build_absolute_uri(pokemon_entitiy.pokemon.image.url)
        )
    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image else None,
            'title_ru': pokemon.title,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(pk=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound(f'<h1>Не найден покемон #{pokemon_id}</h1>')
    pokemon_entities = pokemon.pokemon_entities.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    img_url = request.build_absolute_uri(pokemon.image.url) if pokemon.image else None
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )
    try:
        if pokemon.next_evolution.get():
            if pokemon.next_evolution.get().image:
               img_url = request.build_absolute_uri(
                   pokemon.next_evolution.get().image.url
                   )
            next_evolution = {
                'pokemon_id': pokemon.next_evolution.get().pk,
                'title_ru': pokemon.next_evolution.get().title,
                'img_url': img_url
            }
    except Pokemon.DoesNotExist:
        next_evolution = {}

    previous_evolution = {}
    if pokemon.previous_evolution:
        previous_evolution = {
            'pokemon_id': pokemon.previous_evolution.pk,
            'title_ru': pokemon.previous_evolution.title,
            'img_url': request.build_absolute_uri(pokemon.previous_evolution.image.url),
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': {
            'img_url': img_url,
            'title_ru': pokemon.title,
            "title_en": pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'description': pokemon.description,
            'previous_evolution': previous_evolution,
            'next_evolution': next_evolution,
        }
    })
