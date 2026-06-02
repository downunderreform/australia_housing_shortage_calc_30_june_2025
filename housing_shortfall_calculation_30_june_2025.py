# Australia's Housing Shortage Calculation

# # Overall method
# First we will calculate the number of homes physically present in Australia.
# Then we will calculate the number of homes needed to adequately house Australia's population.
# Then we will compare these numbers, to calculate whether we have more or less homes than we need.

# # Step 1: Calculate the number of homes physically present in Australia
# The starting point is the most recent census, as this is when the ABS does a rigorous count of all homes physically
# present in Australia. Note that this includes both occupied and unoccupied.
# Reference: https://www.abs.gov.au/census/find-census-data/quickstats/2021/AUS
number_of_homes_2021_census = 10852208

# To calculate the number of homes physically present in Australia at the year ends of 2021, 2022 and 2023, and June of
# 2025, we need to  use construction and demolition data, as the 2026 census has not yet been held.
# We are deliberately skipping 2024, as this can be obtained from the NHSAC, as will be explained subsequently.
# The dwellings completed per quarter are taken from the ABS. These numbers are gross, ie not subtracting demolitions.
# Reference: https://www.abs.gov.au/statistics/industry/building-and-construction/building-activity-australia/latest-release#data-downloads (Table 37)
quarterly_gross_dwellings_completed = {
    "Mar-2021": 39051, "Jun-2021": 47552, "Sep-2021": 45601, "Dec-2021": 46356,
    "Mar-2022": 36951, "Jun-2022": 43896,"Sep-2022": 45389, "Dec-2022": 47694,
    "Mar-2023": 38678, "Jun-2023": 42314, "Sep-2023": 45257, "Dec-2023": 49836,
    "Mar-2025": 38001, "Jun-2025":41329, "Sep-2025":45451
}

# Demolition data for 2021, 2022 and 2023 is not available, however the NHSAC published this for 2024.
# So as a best estimate, we will assume the demolition ratios in 2021-3 were the same as 2024
# In 2024, there were 177,000 gross constructions and 155,000 net constructions.
# Therefore, we can calculate the ratio of demolitions to constructions as (177000 - 155000) / 177000
# Reference: https://nhsac.gov.au/sites/nhsac.gov.au/files/2025-05/ar-state-housing-system-2025.pdf (PDF page 13)
demolition_ratio =  (177000 - 155000) / 177000
# We need to know the fraction of homes built that are additional to existing stock, which is calculated by 1 minus the demolition ratio
net_construction_ratio = 1 - demolition_ratio

# Convert quarterly gross dwellings completed data into annual net dwellings completed, aka annual net construction rate
annual_net_construction_rates = {}
annual_net_construction_rates[2021] = sum(list(quarterly_gross_dwellings_completed.values())[:4]) * net_construction_ratio
annual_net_construction_rates[2022] = sum(list(quarterly_gross_dwellings_completed.values())[4:8]) * net_construction_ratio
annual_net_construction_rates[2023] = sum(list(quarterly_gross_dwellings_completed.values())[8:12]) * net_construction_ratio
annual_net_construction_rates[2025] = sum(list(quarterly_gross_dwellings_completed.values())[12:]) / 0.75 * net_construction_ratio

# For 2024, the NHSAC published the net construction data, which was 155,000.
# We will use this to calculate the number of homes in Australia on 30th June, 2024.
# Reference: https://nhsac.gov.au/sites/nhsac.gov.au/files/2025-05/ar-state-housing-system-2025.pdf (PDF page 13)
annual_net_construction_2024 = 155000

# Based on these rates, calculate the number dwellings present in Australia at the end of each year
# Note that the 2021 census was held on August 10, which is 0.6 of the way through the year
year_end_dwellings = {}
year_end_dwellings[2021] = number_of_homes_2021_census + annual_net_construction_rates[2021] * 0.4
year_end_dwellings[2022] = year_end_dwellings[2021] + annual_net_construction_rates[2022]
year_end_dwellings[2023] = year_end_dwellings[2022] + annual_net_construction_rates[2023]
year_end_dwellings[2024] = year_end_dwellings[2023] + annual_net_construction_2024

number_of_dwellings_june_30th_2025 = year_end_dwellings[2024] + annual_net_construction_rates[2025] * 0.5

# However, we need to subtract dwellings not suitable for permanent habitation.
# In the 2021 census, there were 94,925 dwellings categorised as: Caravan, Cabin, houseboat, Improvised home, tent and sleepers out.
# These are not suitable for permanent habitation, so these are subtracted from the number of physical dwellings
# Reference: https://www.abs.gov.au/statistics/people/housing/housing-census/2021/Housing%20data%20summary.xlsx (see table 2)
number_of_permanent_dwellings_june_30th_2025 = number_of_dwellings_june_30th_2025 - 94925

# The total permanent dwellings calculated by the above method was 11,354,187.
# This was cross-referenced against the "Total Value of Dwellings" dataset.
# According to this, there were  11,357,500 residential dwellings in Australia showed as of June 30th, 2025.
# This is within 3,000 of our estimate, providing further support for the accuracy of this figure.
# Reference: https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/total-value-dwellings/dec-quarter-2025/643201.xlsx

# # Step 2: Calculate the number of homes required to adequately accommodate the people in Australia

# The basic approach of all methods is to first calculate the number of required households.
# There are several types of households, such as a family with two parents and children living together, a single
# parent with children, or a shared house. Each type of household contains a different number of people.
# As each household occupies one home, this will determine the number of homes required.
# The number of households is calculated based on the age structure of the population, and the propensity of each age
# group to live in each type of household.
# Overall method reference:
# https://www.abs.gov.au/methodologies/household-and-family-projections-australia-methodology/2021-2046

# Therefore, the first step is to define the below variable, containing the age structure of the population.
# This variable contains the number of people in Australia from ages 0 to 100+, as of 30th June 2025.
# Reference: https://www.abs.gov.au/statistics/people/population/national-state-and-territory-population/latest-release#data-downloads
# Specifically, the table named: Population - Australia: Population at 30 June, by sex and single year of age, Aust.

age_distribution_2025 = \
    [299868, 292641, 297299, 317661, 309974, 308754, 316300, 318696, 325414, 334684, 332482, 335866, 339173, 338931,
     336115, 339736, 337187, 338118, 342149, 347170, 350252, 351531, 355044, 368697, 389343, 398744, 398981, 405125,
     410034, 412703, 418199, 413319, 410965, 408824, 413817, 413260, 405683, 401190, 399125, 399551, 395948, 390993,
     388101, 374835, 363000, 344728, 335895, 325571, 322410, 322462, 324729, 329198, 335994, 347266, 349710, 326201,
     321085, 307473, 300328, 298963, 301761, 309521, 312180, 308617, 304563, 292367, 285544, 278163, 269323, 262716,
     253173, 243949, 239482, 230400, 225718, 218556, 209301, 206733, 207652, 168985, 156548, 143042, 124239, 117064,
     103789, 95250, 85461, 75529, 66329, 56441, 46766, 38396, 32239, 26151, 21925, 17414, 12784, 9193, 6511, 5039, 7345]

# The next step is to define the below variable containing the "living arrangement propensities".
# This variable contains the proportion of each age group residing in each type of household.
# This data is  collected at each census.
# Reference: https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&32360do005_20062031.xls&3236.0&Data%20Cubes&F8A889B31D7CA870CA25773B0017EC1D&0&2006%20to%202031&08.06.2010&Latest
living_propensities_1996 = [
    [0, 0, 0, 0.7, 8.2, 28.5, 53.9, 66.2, 67.1, 59.7, 45.6, 30.8, 19.7, 12.1, 7.3, 4.5, 2.7, 1.4],
    [85.3, 82.8, 80.7, 66.6, 33.4, 11.9, 4.1, 2, 1.1, 0.6, 0.3, 0.1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0.8, 0.7, 0.5, 0.4, 0.2, 0.2, 0.2, 0.3, 0.6, 0.9, 1.3, 1.7, 2.2, 2.7, 2.9],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1.6, 14.5, 25.8, 16.5, 9.5, 10.1, 18.4, 32.5, 46.3, 54.4, 56.7, 53.6, 45.1, 32.3, 15.5],
    [0, 0, 0, 0.5, 0.5, 0.3, 0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 0.5, 0.9, 1.7, 3.3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0.1, 0.1, 0.3, 0.5, 0.9, 1.4, 1.6, 1.4, 1.1, 0.9, 0.8, 0.8, 0.8, 0.9, 1],
    [0, 0, 0, 0.7, 3.1, 4.5, 5.6, 6.5, 6.7, 5.7, 4.4, 3.4, 3.1, 3.1, 3.3, 3.7, 4.2, 4.9],
    [14.6, 17.1, 18.5, 15.1, 7.6, 3.7, 2.1, 1.7, 1.5, 1.4, 1.2, 1, 0.7, 0.3, 0.1, 0, 0, 0],
    [0, 0, 0, 0.5, 0.4, 0.3, 0.2, 0.2, 0.2, 0.2, 0.3, 0.4, 0.5, 0.5, 0.6, 0.7, 0.8, 0.9],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2.1, 3.8, 2.2, 1.1, 0.7, 0.5, 0.5, 0.5, 0.7, 0.9, 1.2, 1.5, 1.7, 1.8, 1.6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4.5, 15.5, 10.4, 5.1, 2.9, 2.3, 2.1, 2.1, 2, 1.9, 1.8, 1.6, 1.5, 1.2, 0.9],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0.8, 3.4, 5.1, 5.3, 5, 4.8, 4.8, 5.1, 5.6, 6.2, 6.9, 7.2, 7.9, 8.4, 7.3],
    [0, 0, 0, 0.8, 2.9, 3.3, 2.9, 2.6, 2.8, 3.5, 4.8, 6.5, 9.2, 13.2, 18.8, 25.3, 29.9, 25.5],
    [0.1, 0.1, 0.8, 3.3, 2.4, 1.3, 0.9, 0.8, 0.7, 0.7, 0.8, 0.9, 1.1, 1.5, 2.6, 5.6, 13.2, 34.6]]

# We also need to know the average number of people per group household and per "other family" household.
# To calculate this, we take weighted means of the 1996 census Basic Community Profiles, which shows the number of
# group households and "other family" households with 1 to 6+ inhabitants, and total of each household type.
# The below are from Table 26 and assume an insignificant number of households with more than 6 inhabitants.
# https://ia801501.us.archive.org/30/items/1996-01-bcp-0-australia/1996_01_BCP_0_Australia.pdf
# These come out to 2.32 for "other family" and 2.33 for group households.
other_family_household_size = (62388 * 2 + 16270 *3 + 3524 * 4 + 731 * 5 + 241 * 6) / 83158
group_household_size = (200273*2 + 48455*3 + 13090*4 + 3026*5 + 1158*6) / 266002

# The age structure table consists of the number of people of each age, from 0 to 100+.
# However, the living propensities are grouped in 5 year age brackets, such as 0-4, up to 85+.
# Therefore, we use the following code to split the age structure table into these brackets
population_by_bracket = {}
for start in range(0, 85, 5):
    end = start + 4
    population_by_bracket[f"{start}-{end}"] = sum(age_distribution_2025[start:end+1])
population_by_bracket["85+"] = sum(age_distribution_2025[85:])

# Now we multiply the number of people in each age bracket by the propensity of that bracket to live in each type of
# household. The sum of these products gives the total number of households, each of which needs one home to live in.
total_households = 0
for i, bracket_population in enumerate(population_by_bracket.values()):
    # Number of partners living in family households with 2 partners. Divide by 2, because 2 partners.
    total_households = total_households + living_propensities_1996[0][i] / 100 * bracket_population / 2
    # Number of partners living in 2 partner households without children. Divide by 2, because 2 partners.
    total_households = total_households + living_propensities_1996[4][i] / 100 * bracket_population / 2
    # Number of male parents living in single parent households with children. Divide by 1, because 1 parent.
    total_households = total_households + living_propensities_1996[7][i] / 100 * bracket_population / 1
    # Number of female parents living in single parent households with children. Divide by 1, because 1 parent.
    total_households = total_households + living_propensities_1996[8][i] / 100 * bracket_population / 1
    # Number of related people living in an "other family" household. Divide by average other family group household size.
    total_households = total_households + living_propensities_1996[12][i] / 100 * bracket_population / group_household_size
    # Number of unrelated people living in an "other family" household. Divide by average other family group household size.
    total_households = total_households + living_propensities_1996[14][i] / 100 * bracket_population / group_household_size
    # Number of males living by themselves. Divide by 1, because 1 person per household.
    total_households = total_households + living_propensities_1996[16][i] / 100 * bracket_population / 1
    # Number of females living by themselves. Divide by 1, because 1 person per household.
    total_households = total_households + living_propensities_1996[17][i] / 100 * bracket_population / 1

# Display the results
print("")
print("The number of households that would form in Australia under affordable housing conditions, as 30th June 2025, was: "
      +  f"{total_households / 1e6:.3f} million")
print("The number of dwellings in Australia, including occupied and unoccupied, as of 30th June 2025, was: "
      + f"{number_of_dwellings_june_30th_2025 / 1e6:.3f} million")
print("")

# However, need to subtract dwellings not suitable for permanent habitation.
# Reference: https://www.abs.gov.au/statistics/people/housing/housing-census/2021/Housing%20data%20summary.xlsx (see table 2)
print("However, in the 2021 census, there were 94,925 dwellings categorised as: Caravan, Cabin, houseboat, Improvised home, tent and sleepers out.")
print("These are not suitable for permanent habitation, so these are subtracted from the number of physical dwellings.")
print("This leaves a total number of physical dwellings of: " + f"{number_of_permanent_dwellings_june_30th_2025 / 1e6:.3f} million")
print("")

# Also, need to subtract dwellings to be used as vacant rental stock, to ensure a non-constrained market.
# 30.6% of households were renting according to the 2021 census.
# Reference: https://www.abs.gov.au/statistics/people/people-and-communities/snapshot-australia/2021#australian-homes
# A typical healthy vacancy rate is 3%
# Reference: https://www.realestate.com.au/insights/where-rental-vacancy-has-hit-an-all-time-low/
# Therefore we need to subtract 3% of the renting households from the total physical stock, to be used as vacancies
number_rental_vacancy_homes = total_households * 0.306 * 0.03
print("However, economists recommend that in order for a rental market to be healthy, there needs to be 3% vacancy rate.")
print("This means we need to add: " + f"{number_rental_vacancy_homes/ 1e6:.3f}"  + " million to the number of homes needed")
print("This gives the total number of homes needed as: "  +  f"{(total_households + number_rental_vacancy_homes)/ 1e6:.3f} million")
print("")

# Additionally, we need to have some vacant homes for sale.
# Analysts state: "A balanced real estate market is characterized by an equilibrium between the number of
# homes available for sale and the demand from potential buyers. This state occurs when there is approximately
# 5 to 7 months of inventory"
# Reference: https://www.jchs.harvard.edu/blog/existing-inventories-historically-low-homebuyers-turn-new-home-market
# ABS data shows there were 549,147 property transfers in 2024
# Reference: https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/total-value-dwellings/jun-quarter-2025/643202.xlsx
# Therefore we need to add 50% of 549,147 to the number of homes required
number_vacant_homes_for_sale = 549147 * 0.5
total_homes_needed = total_households + number_rental_vacancy_homes + number_vacant_homes_for_sale
print("However, analysts recommend that in order for a home purchase market to be healthy, there needs to be 6 months of unoccupied homes on the market.")
print("In 2024, there were 549,147 home sales according to the ABS.")
print("This means we need to add: " +  f"{number_vacant_homes_for_sale / 1e6:.3f}" + " million to the number of homes needed")
print("This gives the total number of homes needed as: " + f"{total_homes_needed / 1e6:.3f}" + " million")
print("")

print("Remember we had a total number of physical dwellings of: " +  f"{number_of_permanent_dwellings_june_30th_2025 / 1e6:.3f}" + " million")
print("Even with just the allowances mentioned above, the total number of homes needed is: " + f"{total_homes_needed / 1e6:.3f}" + " million")
print("This means that even in the perfect distribution scenario, there would be a shortage of: "
      + f"{(number_of_permanent_dwellings_june_30th_2025 - total_homes_needed) / 1e6 * -1:.3f}"  " million homes")
