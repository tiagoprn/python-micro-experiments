# Below I build a tuple with just the is_important airports. 

important_airports = (airport for airport in airports if airport.is_important)
