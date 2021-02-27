# Similarity analysis between legislators

After going through all their votes, it turns out they all largely vote the same
when it comes to voting for any `action` that has a street name it titles. Here
is an example:

```
PS C:\Users\ivand\Documents\programs\voting_recording_research> python .\main.py get_overlap "dean_preston" "rafeal_mandelman"
Number of similar votes: 351
Number of dissimilar votes: 10
Percentage of agreement amongst actions where they both were elected: % 97.23
Percentage of disagreement amongst actions where they were elected: % 2.77
------------------------------
Hearing of persons interested in or objecting to the decision of Public Works, dated December 7, 2020, disapproving a Tentative Map for a six unit condominium conversion at 424, 426, 428, 430, 432, and 434 Francisco Street, Assessor's Parcel Block No. 0041, Lot No. 010. (District 3) (Appellant: Scott Emblidge of Moscone Emblidge & Rubens, on behalf of the Owners of 424, 426, 428, 430, 432, and 434 Francisco Street) (Filed December 14, 2020)
dean_preston: Excused
rafeal_mandelman: Aye
----------------------------
Motion approving the decision of Public Works and disapproving the Tentative Map for a six unit condominium conversion at 424, 426, 428, 430, 432, and 434 Francisco Street, Assessor's Parcel Block No. 0041, Lot No. 010.
dean_preston: Excused
rafeal_mandelman: Aye
----------------------------
Motion conditionally disapproving the decision of Public Works and approving the Tentative Map for a six unit condominium conversion at 424, 426, 428, 430, 432, and 434 Francisco Street, Assessor's Parcel Block No. 0041, Lot No. 010, subject to the Board of Supervisors’ adoption of written findings in support of the disapproval.
dean_preston: Excused
rafeal_mandelman: Aye
----------------------------
Motion directing the Clerk of the Board to prepare findings relating to the Board of Supervisors' decision to approve the Tentative Map for a six unit condominium conversion at 424, 426, 428, 430, 432, and 434 Francisco Street, Assessor's Parcel Block No. 0041, Lot No. 010.
dean_preston: Excused
rafeal_mandelman: Aye
----------------------------
Motion appointing Supervisor Rafael Mandelman, term ending December 1, 2021, to the California State Association of Counties.
dean_preston: Aye
rafeal_mandelman: Excused
----------------------------
Resolution authorizing and approving a Lease with NPU, Inc., a California corporation, for the United States Old Mint at 88 Fifth Street, at the monthly base rent of $22,000; requiring tenant to be responsible for all utilities and services, participation rent of 50% of venue rental fees and $2,500 per ticketed event subject to a rent credit not to exceed $500,000 for a two-year term to commence upon approval by the Board of Supervisors and Mayor through February 28, 2022, with three one-year options to extend; authorizing the Director of Property to execute documents, make certain modificatio
dean_preston: Aye
rafeal_mandelman: Absent
----------------------------
Motion affirming the determination by the Planning Department that the proposed San Francisco Municipal Transportation Agency Page Street Bikeway Improvements Pilot Project is categorically exempt from further environmental review.
dean_preston: Aye
rafeal_mandelman: Absent
----------------------------
Motion conditionally reversing the determination by the Planning Department that the San Francisco Municipal Transportation Agency Page Street Bikeway Improvements Pilot Project is categorically exempt from further environmental review, subject to the adoption of written 
findings by the Board in support of this determination.
dean_preston: Aye
rafeal_mandelman: Absent
----------------------------
Motion directing the Clerk of the Board to prepare findings reversing the determination by the Planning Department that the proposed San Francisco Municipal Transportation Agency Page Street Bikeway Improvements Pilot Project is categorically exempt from further environmental review.
dean_preston: Aye
rafeal_mandelman: Absent
----------------------------
Hearing of persons interested in or objecting to the determination of exemption from environmental review under the California Environmental Quality Act issued as a Categorical Exemption by the Planning Department on September 6, 2019, approved on November 19, 2019, for the San Francisco Municipal Transportation Agency's proposed Page Street Bikeway Improvements Pilot Project involving a 12-month pilot to study the effects of several traffic circulation changes to the area bounded by Fell Street to the north, Market, Gough, and Otis Streets to the south, Fillmore Street to the west, and Gough
dean_preston: Aye
rafeal_mandelman: Absent
----------------------------
```

They only reason there are even differences is because one or the other was simply not there. Its probably reasonable to assume that they would've voted the same
