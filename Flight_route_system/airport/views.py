from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Airport
from .forms import AirportForm, AddNextAirportForm, ShortestPathForm,NthNodeForm,DurationForm
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



@login_required
def shortest_path_view(request):
    """
    View function to handle finding the shortest paths 
    from a selected airport to all other reachable airports.
    """
    result = None

    # ✅ When form is submitted via POST
    if request.method == 'POST':
        form = ShortestPathForm(request.POST)
        if form.is_valid():
            # Normalize the starting airport code to uppercase
            start = form.cleaned_data['start'].strip().upper()

            # Call function to compute shortest paths
            result = find_shortest_path(start)
    else:
        # ✅ When the page is first loaded (GET request)
        form = ShortestPathForm()

    # ✅ Render result (either message or list of airports)
    return render(request, 'airports/shortest_path.html', {
        'form': form,
        'result': result
    })


def find_shortest_path(start_code):
    """
    Finds the shortest travel duration from the given start airport
    to all other connected airports using Dijkstra’s algorithm.
    """
    airports = Airport.objects.all()
    graph = {}

    # ✅ STEP 1: Build a bidirectional graph using airport connections
    for a in airports:
        code = a.code.upper()
        if code not in graph:
            graph[code] = {}

        # Left connection (if exists)
        if a.left and a.left_distance:
            left_code = a.left.code.upper()
            graph[code][left_code] = a.left_distance

            # Add reverse link (bidirectional)
            if left_code not in graph:
                graph[left_code] = {}
            graph[left_code][code] = a.left_distance

        # Right connection (if exists)
        if a.right and a.right_distance:
            right_code = a.right.code.upper()
            graph[code][right_code] = a.right_distance

            # Add reverse link (bidirectional)
            if right_code not in graph:
                graph[right_code] = {}
            graph[right_code][code] = a.right_distance

    # ✅ STEP 2: Validate start airport
    if start_code not in graph:
        return "No nearby airport found."

    # ✅ STEP 3: Initialize Dijkstra’s algorithm
    queue = [(0, start_code)]      # Priority queue with (distance, airport)
    distances = {start_code: 0}    # Dictionary to store shortest distances
    visited = set()                # Set to track visited airports

    # ✅ STEP 4: Explore graph using Dijkstra’s logic
    while queue:
        dist, node = heapq.heappop(queue)

        # Skip if already visited
        if node in visited:
            continue
        visited.add(node)

        # Explore all connected neighbors
        for neighbor, d in graph[node].items():
            new_dist = dist + d
            # If new distance is shorter, update and push into heap
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(queue, (new_dist, neighbor))

    # ✅ STEP 5: Remove the start node from results (no need to show distance to itself)
    distances.pop(start_code, None)

    # ✅ STEP 6: Handle isolated airport
    if not distances:
        return "No nearby airport found."

    # ✅ STEP 7: Sort airports by distance (ascending order)
    sorted_airports = sorted(distances.items(), key=lambda x: x[1])

    # ✅ STEP 8: Return a structured dictionary for template rendering
    # This can be used in HTML to display a list of reachable airports with durations.
    return {
        'airports': sorted_airports,
        'start': start_code
    }


@login_required
def airport_route_view(request):
    # Get the type of search user selected from the query string
    # Default search type is 'duration_between'
    search_type = request.GET.get('type', 'duration_between')
    result = None
    form = None

    # ========== CASE 1: Find Nth Node ==========
    if search_type == 'nth_node':
        if request.method == 'POST':
            form = NthNodeForm(request.POST)
            if form.is_valid():
                # Read form values and normalize inputs
                start = form.cleaned_data['start'].strip().upper()
                direction = form.cleaned_data['direction']
                n = form.cleaned_data['n']
                # Call logic to find nth left/right node
                result = find_nth_node(start, direction, n)
        else:
            form = NthNodeForm()

    # ========== CASE 2: Duration Between Two Airports ==========
    elif search_type == 'duration_between':
        if request.method == 'POST':
            form = DurationForm(request.POST)
            if form.is_valid():
                # Read starting and ending airport codes
                from_airport = form.cleaned_data['from_airport'].strip().upper()
                to_airport = form.cleaned_data['to_airport'].strip().upper()
                # Call logic to find shortest travel duration
                result = find_duration_between(from_airport, to_airport)
        else:
            form = DurationForm()

    # ========== CASE 3: Find Longest Route ==========
    elif search_type == 'longest_route':
        # Directly call the longest route function
        result = find_longest_route()

    # Render the template with the form, search type, and result
    return render(request, 'airports/route_search.html', {
        'form': form,
        'search_type': search_type,
        'result': result
    })


# ======================= LOGIC FUNCTIONS =======================

def find_nth_node(start_code, direction, n):
    """Find the nth left or right connected airport from a given starting airport."""
    try:
        # Get the starting airport object
        airport = Airport.objects.get(code__iexact=start_code)
    except Airport.DoesNotExist:
        return f"Airport '{start_code}' not found."

    current = airport
    # Move n times in the given direction (left/right)
    for i in range(n):
        next_airport = getattr(current, direction, None)
        if not next_airport:
            return f"No {direction} node found at step {i+1} from {start_code}."
        current = next_airport

    return f"The {n}th {direction} node from {start_code} is {current.code}."


def find_longest_route():
    """Find the longest available direct route (based on distance/duration)."""
    airports = Airport.objects.all()
    longest = None
    max_distance = 0

    # Loop through all airports and compare left and right route distances
    for a in airports:
        # Check left route
        if a.left_distance and a.left_distance > max_distance:
            max_distance = a.left_distance
            longest = (a.code, a.left.code, a.left_distance)
        # Check right route
        if a.right_distance and a.right_distance > max_distance:
            max_distance = a.right_distance
            longest = (a.code, a.right.code, a.right_distance)

    # Return result message
    if longest:
        return f"The longest route is between {longest[0]} and {longest[1]} with duration {longest[2]}."
    return "No route data available."


def find_duration_between(start_code, end_code):
    """Find the shortest duration between two airports using Dijkstra’s algorithm."""
    airports = Airport.objects.all()
    graph = {}

    # Build graph connections with both left and right routes
    for a in airports:
        code = a.code.upper()
        if code not in graph:
            graph[code] = {}

        # Add bidirectional connection for left route
        if a.left and a.left_distance:
            graph[code][a.left.code.upper()] = a.left_distance
            graph[a.left.code.upper()] = graph.get(a.left.code.upper(), {})
            graph[a.left.code.upper()][code] = a.left_distance

        # Add bidirectional connection for right route
        if a.right and a.right_distance:
            graph[code][a.right.code.upper()] = a.right_distance
            graph[a.right.code.upper()] = graph.get(a.right.code.upper(), {})
            graph[a.right.code.upper()][code] = a.right_distance

    # Validate start and end codes
    if start_code not in graph or end_code not in graph:
        return "Invalid airport code."

    # Apply Dijkstra’s shortest path algorithm
    queue = [(0, start_code)]      # Priority queue with (distance, airport)
    distances = {start_code: 0}    # Store shortest known distances
    visited = set()                # Track visited airports

    while queue:
        dist, node = heapq.heappop(queue)

        # If we reach the destination, return total duration
        if node == end_code:
            return f"Shortest duration from {start_code} to {end_code} is {dist}."

        # Skip already visited nodes
        if node in visited:
            continue
        visited.add(node)

        # Explore neighbors and update distances
        for neighbor, d in graph[node].items():
            new_dist = dist + d
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(queue, (new_dist, neighbor))

    # If no path found between the airports
    return f"No route found between {start_code} and {end_code}."
