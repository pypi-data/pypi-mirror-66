payload = {"FlightAttributes":[{"flightNumber":"231","dateOfFlight":"2020-03-25","timeOfFlight":"12:30","flyTime":"6","loadfactor":"83.23","origin":"AYT","destination":"FRA","fareClass":"Y","carrier":"XQ"}],"ProductAttributes":[{"seatAttribute":"[XLEG,EMERGENCYEXIT]","price":"40","ancillaryType":"ANCILLARY SEAT"}],"LoyaltyAttributes":[{"membershipNumber":12432}],"PassengerAttributes":[{"posCountry":"TR","pnrType":"NORMAL","age":"45","currencyCode":"EUR","fareType":"BASE","countryOfOrigin":"IN"}],"flightModel":"true","paxModel":"true","persona":"false","productModel":"false","loyaltyModel":"false"}
for i in range (100) :

	payload["FlightAttributes"][0]["flyTime"] = str(i*10)
	
	print ( payload)
