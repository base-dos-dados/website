from .attr_enum import AttrEnum
from enum import Enum
from typing import Union


class ObservationLevelSphereEnum(AttrEnum):
    continent        = {'label': "Continent"}
    country          = {'label': "Country"}
    region           = {'label': "Region"}
    state            = {'label': "State"}
    county           = {'label': "County"}
    district         = {'label': "District"}
    municipality     = {'label': "Municipality"}
    city             = {'label': "City"}
    village          = {'label': "Village"}
    neighborhood     = {'label': "Neighborhood"}
    zip_code         = {'label': "Zip Code"}
    census_tract     = {'label': "CensusTract"}


class ObservationLevelIndividualEnum(AttrEnum):
    person           = {'label': "Person (student, teacher/professor, politician/candidate, player, partner, etc)"}
    household        = {'label': "Household"}
    name             = {'label': "Name"}
    animal           = {'label': "Animal"}
    plant            = {'label': "Plant"}


class ObservationLevelEstablishmentEnum(AttrEnum):
    agency           = {'label': "Agency"}
    protected_area   = {'label': "Protected Area"}
    library          = {'label': "Library"}
    notary_office    = {'label': "Notary's Office"}
    company          = {'label': "Company"}
    school           = {'label': "School"}
    station          = {'label': "Station"}
    stadium          = {'label': "Stadium"}
    terrorist_group  = {'label': "Terrorist Group"}
    hospital         = {'label': "Hospital"}
    property         = {'label': "Property"}
    ministry         = {'label': "Ministry/Department"}
    museum           = {'label': "Museum"}
    ngo              = {'label': "Nongovernmental Organization (NGO)"}
    prison           = {'label': "Prison"}
    team             = {'label': "Team"}
    university       = {'label': "University"}


class ObservationLevelPoliticsEnum(AttrEnum):
    agreement        = {'label': "Agreement/Treaty"}
    speech           = {'label': "Speech"}
    election         = {'label': "Election"}
    law              = {'label': "Law/Proposition"}
    party            = {'label': "Party"}
    poll             = {'label': "Poll"}


class ObservationLevelScienceEnum(AttrEnum):
    article          = {'label': "Article/Paper"}
    citation         = {'label': "Citation"}
    domain           = {'label': "Domain"}
    book             = {'label': "Book"}
    newspaper        = {'label': "Newspaper"}
    patent           = {'label': "Patent"}
    journal          = {'label': "Journal/Magazine"}
    word             = {'label': "Word"}
    post             = {'label': "Post/Tweet"}
    langugage        = {'label': "Language"}
    crs              = {'label': "Coordinate Reference System"}
    protein          = {'label': "Protein"}
    meteor           = {'label': "Meteor"}


class ObservationLevelEconomicsEnum(AttrEnum):
    contract         = {'label': "Contract"}
    grant            = {'label': "Grant"}
    procurement      = {'label': "Procurement"}
    product          = {'label': "Product"}
    transaction      = {'label': "Transaction"}
    transfer         = {'label': "Transfer"}
    bill             = {'label': "Money Bill"}
    occupation       = {'label': "Occupation"}
    sector           = {'label': "Sector"}


class ObservationLevelEducationEnum(AttrEnum):
    scholarship      = {'label': "Scholarship"}
    test             = {'label': "Test/Exam"}


class ObservationLevelEventsEnum(AttrEnum):
    alert            = {'label': "Alert"}
    attack           = {'label': "Attack"}
    act              = {'label': "Act"}
    concert          = {'label': "Concert"}
    disinvitation    = {'label': "Disinvitation"}
    disaster         = {'label': "Natural Disaster (earthquake, flood, fire, etc)"}
    birth            = {'label': "Birth"}
    death            = {'label': "Death"}
    request          = {'label': "Request/Complaint"}
    protest          = {'label': "Protest"}
    match            = {'label': "Match"}

class ObservationLevelArtEnum(AttrEnum):
    album            = {'label': "Album"}
    movie            = {'label': "Movie/Film/Clip/Show"}
    photo            = {'label': "Photo/Picture"}
    song             = {'label': "Song"}
    statue           = {'label': "Statue"}
    painting         = {'label': "Painting/Drawing/Illustration"}
    poem             = {'label': "Poem"}
    roller_coaster   = {'label': "Roller Coaster"}

class ObservationLevelInfrastructureEnum(AttrEnum):
    dam              = {'label': "Dam"}
    satellitte       = {'label': "Satellite"}
    street_road      = {'label': "Street/Avenue/Road/Highway"}


class ObservationLevelTransportationEnum(AttrEnum):
    automobile       = {'label': "Car/Bus/Truck/Motorcycle"}
    train            = {'label': "Train"}
    aircraft         = {'label': "Plane/Helicopter"}
    ship             = {'label': "Ship"}

class ObservationLevelSecurityEnum(AttrEnum):
    gun              = {'label': "Gun"}


class ObservationLevelDemographicEnum(AttrEnum):
    age              = {'label': "Age"}
    race             = {'label': "Race/Skin color"}
    sex              = {'label': "Sex"}


class ObservationLevelImageEnum(AttrEnum):
    pixel            = {'label': "Pixel/Grid"}
    polygon          = {'label': "Polygon"}


class ObservationLevelHistoryEnum(AttrEnum):
    empire           = {'label': "Empire"}


class ObservationLevelOthersEnum(AttrEnum):
    other            = {'label': "Other"}


ObservationLevel = Union[
    ObservationLevelSphereEnum,
    ObservationLevelIndividualEnum,
    ObservationLevelEstablishmentEnum,
    ObservationLevelPoliticsEnum,
    ObservationLevelScienceEnum,
    ObservationLevelEconomicsEnum,
    ObservationLevelEducationEnum,
    ObservationLevelEventsEnum,
    ObservationLevelArtEnum,
    ObservationLevelInfrastructureEnum,
    ObservationLevelTransportationEnum,
    ObservationLevelSecurityEnum,
    ObservationLevelDemographicEnum,
    ObservationLevelHistoryEnum,
    ObservationLevelOthersEnum,
]
