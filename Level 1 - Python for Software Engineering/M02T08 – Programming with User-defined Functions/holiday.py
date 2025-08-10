"""
Holiday Cost Calculator

This script calculates the total cost of a holiday, including hotel stay, flight, and car rental.
"""

def hotel_cost(num_nights):
    """
    Calculate the total cost for the hotel stay.

    Args:
        num_nights (int): Number of nights to stay at the hotel.

    Returns:
        int: Total hotel cost in South African Rand (ZAR).
    """
    price_per_night = 1200.50  # Cost per night in ZAR (float)
    return num_nights * price_per_night


def plane_cost(city_flight):
    """
    Calculate the cost of the flight based on the selected South African city.

    Args:
        city_flight (str): The city to which the user will fly.

    Returns:
        int: Flight cost in South African Rand (ZAR).
    """
    city = city_flight.strip().lower()
    if city == "cape town":
        return 2500.75
    elif city == "durban":
        return 1800.40
    elif city == "johannesburg":
        return 2200.99
    elif city == "port elizabeth":
        return 2000.25
    else:
        print("Warning: City not recognized. Using default flight price.")
        return 2100.00  # Default price for other cities


def car_rental(rental_days):
    """
    Calculate the total cost for car rental.

    Args:
        rental_days (int): Number of days to rent the car.

    Returns:
        int: Total car rental cost in South African Rand (ZAR).
    """
    daily_rate = 400.80  # Cost per day in ZAR (float)
    return rental_days * daily_rate


def holiday_cost(num_nights, city_flight, rental_days):
    """
    Calculate the total holiday cost including hotel, flight, and car rental.

    Args:
        num_nights (int): Number of nights at the hotel.
        city_flight (str): Destination city for the flight.
        rental_days (int): Number of days for car rental.

    Returns:
        int: Total holiday cost in South African Rand (ZAR).
    """
    return (
        hotel_cost(num_nights)
        + plane_cost(city_flight)
        + car_rental(rental_days)
    )


def main():
    """Main function to run the holiday cost calculator."""
    available_cities = ["Cape Town", "Durban", "Johannesburg", "Port Elizabeth"]
    print("Available cities: " + ", ".join(available_cities))
    city_flight = input("Enter the South African city you will be flying to: ")

    while True:
        try:
            num_nights = int(input("Enter the number of nights you will stay at the hotel: "))
            break
        except ValueError:
            print("Please enter a valid integer for the number of nights.")

    while True:
        try:
            rental_days = int(input("Enter the number of days you will rent a car: "))
            break
        except ValueError:
            print("Please enter a valid integer for the number of rental days.")

    total_hotel = hotel_cost(num_nights)
    total_plane = plane_cost(city_flight)
    total_car = car_rental(rental_days)
    total = holiday_cost(num_nights, city_flight, rental_days)

    print("\n--- Holiday Summary ---")
    print(f"Destination: {city_flight.title()}")
    print(f"Hotel stay: {num_nights} nights x R1200.50 = R{total_hotel:.2f}")
    print(f"Flight cost: R{total_plane:.2f}")
    print(f"Car rental: {rental_days} days x R400.80 = R{total_car:.2f}")
    print(f"Total holiday cost: R{total:.2f}")


if __name__ == "__main__":
    main()


