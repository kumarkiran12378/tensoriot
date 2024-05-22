import random
import json
import boto3

class Car:
    def __init__(self, license_plate):
        if len(license_plate) != 7:
            raise ValueError("License plate must be of a 7 digit.")
        self.license_plate = license_plate
    
    def __str__(self):
        return self.license_plate
    
    def park(self, parking_lot, spot):
        # Car park function.
        if parking_lot.spots[spot] == None:
            parking_lot.spots[spot] = self
            return True, F'at parking spot {spot}.'
        else:
            return False, 'Parking lot is full.'


class Parkinglot:

    def __init__(self, square_footage, spot_length=12, spot_width=8):
        self.spot_length = spot_length
        self.spot_width = spot_width
        self.spot_area = self.spot_length * self.spot_width
        self.num_spots = square_footage // self.spot_area
        self.spots = [None] * self.num_spots
    
    def is_full(self):
        return all(self.spots)
    
    def park_car(self, car):
        if self.is_full():
            return False, 'Parking lot is full.'
        
        spot = random.randint(0, self.num_spots - 1)
        while self.spots[spot] is not None:
            spot = random.randint(0, self.num_spots -1)
        
        return car.park(self, spot)
    
    def map_parked_cars(self):
        mapping  = {}
        for i , spot in enumerate(self.spots):
            if spot:
                mapping[i] = str(spot)
        return mapping

def save_to_s3(filename):
    s3 = boto3.client('s3')
    bucket_name = 'parking_bucket'
    s3.upload_file(filename, bucket_name, filename)


def main():
    parking_lot_size = 2000

    cars = [Car(str(random.randint(1000000, 9999999))) for _ in range(20)]

    parking_lot = Parkinglot(parking_lot_size)

    while cars and not parking_lot.is_full():
        car = cars.pop()
        success, message = parking_lot.park_car(car)
        if success:
            print(F"Car with license plate {car} parked successfully {message}")
        else:
            print(F"Failed to part with license plase {car}:{message}")

    if parking_lot.is_full():
        print("Parking lot is full.")
    
    mapping = parking_lot.map_parked_cars()

    with open('parking_lot_mapping.json', 'w') as file:
        json.dump(mapping, file)
        print("Parking lot details saved with file name parking_lot_mapping.json .")

    # Upload file to S3.
    # this function is commented as s3 is not linked to account.
    # save_to_s3('parking_lot_mapping.json')

if __name__ == "__main__":
    main()

