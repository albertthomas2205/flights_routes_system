from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Airport
from .forms import AirportForm, AddNextAirportForm, ShortestPathForm
import heapq
# --- Role check decorator ---
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin:
            return render(request, '403.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper


# --- CRUD views ---
@login_required
def airport_list(request):
    query = request.GET.get('q', '')
    airports = Airport.objects.filter(code__icontains=query) if query else Airport.objects.all()
    return render(request, 'airports/airport_list.html', {'airports': airports, 'query': query})


@login_required
@admin_required
def airport_create(request):
    if request.method == 'POST':
        form = AirportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('airport_list')
    else:
        form = AirportForm()
    return render(request, 'airports/airport_form.html', {'form': form, 'title': 'Add Airport'})


@login_required
@admin_required
def airport_update(request, pk):
    airport = get_object_or_404(Airport, pk=pk)
    if request.method == 'POST':
        form = AirportForm(request.POST, instance=airport)
        if form.is_valid():
            form.save()
            return redirect('airport_list')
    else:
        form = AirportForm(instance=airport)
    return render(request, 'airports/airport_form.html', {'form': form, 'title': 'Edit Airport'})


@login_required
@admin_required
def airport_delete(request, pk):
    airport = get_object_or_404(Airport, pk=pk)
    if request.method == 'POST':
        airport.delete()
        return redirect('airport_list')
    return render(request, 'airports/airport_confirm_delete.html', {'airport': airport})


# --- Add next airport (custom logic) ---
@login_required
@admin_required
def add_next_airport_view(request):
    if request.method == 'POST':
        form = AddNextAirportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('airport_list')
    else:
        form = AddNextAirportForm()
    return render(request, 'airports/add_next_airport.html', {'form': form})


# --- Shortest path using Dijkstra ---
# @login_required
# def shortest_path_view(request):
#     result = None
#     if request.method == 'POST':
#         form = ShortestPathForm(request.POST)
#         if form.is_valid():
#             start = form.cleaned_data['start']
#             end = form.cleaned_data['end']
#             result = find_shortest_path(start, end)
#     else:
#         form = ShortestPathForm()
#     return render(request, 'airports/shortest_path.html', {'form': form, 'result': result})


# def find_shortest_path(start_code, end_code):
#     airports = Airport.objects.all()
#     graph = {}

#     for a in airports:
#         graph[a.code] = {}
#         if a.left and a.left_distance:
#             graph[a.code][a.left.code] = a.left_distance
#         if a.right and a.right_distance:
#             graph[a.code][a.right.code] = a.right_distance

#     if start_code not in graph or end_code not in graph:
#         return "Invalid airport codes."

#     # Dijkstra's Algorithm
#     queue = [(0, start_code, [])]
#     visited = set()

#     while queue:
#         (dist, node, path) = heapq.heappop(queue)
#         if node in visited:
#             continue
#         path = path + [node]
#         visited.add(node)

#         if node == end_code:
#             return {'distance': dist, 'path': ' -> '.join(path)}

#         for neighbor, d in graph[node].items():
#             if neighbor not in visited:
#                 heapq.heappush(queue, (dist + d, neighbor, path))

#     return "No path found."

# def find_shortest_path(start_code):
#     try:
#         airport = Airport.objects.get(code=start_code)
#     except Airport.DoesNotExist:
#         return "Airport not found"

#     nearest = []
#     if airport.left:
#         nearest.append((airport.left.code, airport.left_distance))
#     if airport.right:
#         nearest.append((airport.right.code, airport.right_distance))
    
#     if not nearest:
#         return "No connected airports"

#     # Sort by distance
#     nearest.sort(key=lambda x: x[1])
#     return nearest[0]  # Returns tuple: (airport_code, distance)







@login_required
def shortest_path_view(request):
    result = None
    if request.method == 'POST':
        form = ShortestPathForm(request.POST)
        if form.is_valid():
            # Normalize input to uppercase
            start = form.cleaned_data['start'].strip().upper()
            result = find_shortest_path(start)
    else:
        form = ShortestPathForm()

    return render(request, 'airports/shortest_path.html', {'form': form, 'result': result})


def find_shortest_path(start_code):
    airports = Airport.objects.all()
    graph = {}

    # ✅ Build bidirectional graph with UPPERCASE codes
    for a in airports:
        code = a.code.upper()
        if code not in graph:
            graph[code] = {}

        if a.left and a.left_distance:
            left_code = a.left.code.upper()
            graph[code][left_code] = a.left_distance

            if left_code not in graph:
                graph[left_code] = {}
            graph[left_code][code] = a.left_distance

        if a.right and a.right_distance:
            right_code = a.right.code.upper()
            graph[code][right_code] = a.right_distance

            if right_code not in graph:
                graph[right_code] = {}
            graph[right_code][code] = a.right_distance

    # ✅ Handle invalid or disconnected airport
    if start_code not in graph:
        return "No nearby airport found."

    # ✅ Dijkstra’s algorithm
    queue = [(0, start_code)]
    distances = {start_code: 0}
    visited = set()

    while queue:
        dist, node = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)

        for neighbor, d in graph[node].items():
            new_dist = dist + d
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(queue, (new_dist, neighbor))

    # ✅ Remove start node itself
    distances.pop(start_code, None)

    if not distances:
        return "No nearby airport found."

    # ✅ Sort by distance ascending
    sorted_airports = sorted(distances.items(), key=lambda x: x[1])

    # ✅ Return dict for template rendering
    return {'airports': sorted_airports, 'start': start_code}