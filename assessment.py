# class Venue:
#     all=[ ]
#     def __init__(self, name, city):
#         self.name = name
#         self.city = city
# 
#     @property
#     def name(self):
#         return self._name
#     
#     @name.setter
#     def name(self, name):
#         if not isinstance(name, str):
#             raise TypeError("Names must be of type str")
#         elif not len(name):
#             raise ValueError("Names must contain at least one character")
#         else:
#             self._name = name
#     
#     @property
#     def city(self):
#         return self._city
#     
#     @city.setter
#     def city(self, city):
#         if not isinstance(city, str):
#             raise TypeError("City must be of type str")
#         elif not len(city):
#             raise ValueError("City must contain at least one character")
#         else:
#             self._city = city
# 
#     def concerts(self):
#         #! Build the association method that retrieves all concerts for a specific venue
#         ''' get all concerts associated with the venue'''
#         return [concert for concert in Concert.all_ if concert.venue == self]
#         
#     @classmethod
#     def venue_with_most_concerts(cls):
#         #! Build a class method called venue_with_most_concerts, that retrieves the venue with the most concerts if any 
#         venue_concert_counts = {}
#         for concert in Concert.all_:
#             venue = concert.venue
#             # Increment the count for this venue in the dictionary
#             if venue in venue_concert_counts:
#                 venue_concert_counts[venue] += 1
#             else:
#                 venue_concert_counts[venue] = 1
#         # Return the venue with the highest concert count, or None if no concerts
#         return max(venue_concert_counts, key=venue_concert_counts.get) if venue_concert_counts else None
# 
# class Concert:
#     all_ = []
#     def __init__(self, date, band, venue):
#         self.date = date
#         self.band = band
#         self.venue = venue
#         type(self).all_.append(self)
#     
#     @property
#     def date(self):
#         return self._date
#     
#     @date.setter
#     def date(self, date):
#         if not isinstance(date, str):
#             raise TypeError("Date must be of type str")
#         elif not len(date):
#             raise ValueError("Date must contain at least one character")
#         else:
#             self._date = date
#     
#     @property
#     def band(self):
#         return self._band
#     
#     @band.setter
#     def band(self, band):
#         if not isinstance(band, str):
#             raise TypeError("band must be of type str")
#         elif not len(band):
#             raise ValueError("band must contain at least one character")
#         else:
#             self._band = band
# 
#     @property
#     def venue(self):
#         return self._venue
#     
#     @venue.setter
#     def venue(self, venue):
#         if not isinstance(venue, Venue):
#             raise TypeError("Venue must be of type Venue")
#         else:
#             self._venue = venue