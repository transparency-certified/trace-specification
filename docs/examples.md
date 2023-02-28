(trace-examples)=
# Examples

The following are examples of research published to journals with transparency
and reproducibility policies that would benefit from TRACE. 

(example-rdc)=
## RDC 

Mogstad, Magne, Alexander Torgovitsky, and Christopher R. Walters. 2021. "The
Causal Interpretation of Two-Stage Least Squares with Multiple Instrumental
Variables." American Economic Review 111(11): 3663–98.
[Paper](https://doi.org/10.1257/aer.20190221) [Replication
package](https://doi.org/10.3886/E135041V1)

* Uses confidential data from the BLS National Longitudinal Survey of Youth
* Researchers can gain access to the BLS data, but the environment has changed
  since the original authors had access (access protocols have changed).

Berger, David, Kyle Herkenhoff, and Simon Mongey. 2022. "Labor Market Power."
American Economic Review 112(4): 1147–93. [Replication
package](https://doi.org/10.3886/E154241V2)
* Uses confidential [Census data](caseprofile-rdc), passed disclosure avoidance review

Yeh, Chen, Claudia Macaluso, and Brad Hershbein. 2022. "Monopsony in the US
Labor Market." American Economic Review 112(7): 2099–2138.
[Paper](https://www.aeaweb.org/articles?id=10.1257/aer.20200025) [Replication
package](https://doi.org/10.3886/E162581V1)

* Uses confidential [Census data](caseprofile-rdc), passed disclosure avoidance review


(example-specialized-compute)=
## Large or specialized compute

Rudik, Ivan. 2020. "Optimal Climate Policy When Damages Are Unknown." American
Economic Journal: Economic Policy 12(2): 340–73. [Paper](https://doi.org/10.1257/pol.20160541) [Replication
package](https://doi.org/10.3886/E111185V1)
* Original execution required >20,000 core hours

Desmet, Klaus et al. 2021. "Evaluating the Economic Cost of Coastal Flooding."
American Economic Journal: Macroeconomics 13(2): 444–86.
[Paper](https://doi.org/10.1257/mac.20180366)
[Replication Package](https://doi.org/10.3886/E117946V1)
* Requires 12 cores, 512GB RAM and ~3TB fast local storage. Run time was >12 hours.

Webb, Clayton; Linn, Suzanna; Lebo, Matthew, 2019, "Replication Data for: Beyond
the Unit Root Question: Uncertainty and Inference",
[Replication package](https://doi.org/10.7910/DVN/ZBRTJH)
* Simulations were performed on the University of Kansas High Performance
  Compute Cluster with each job requesting 4 nodes with 20 cores per node.
* Odum could not reproduce results on UNC cluster due to software
  incompatibilities, but was successful using Docker on a large VM.

Sanford, Luke, 2021, "Replication Data for: Democratization, Elections, and
Public Goods: The Evidence from Deforestation",
[Replication package](https://doi.org/10.7910/DVN/EF7R0Z)
* Used UCSD's Social Science Research and Development Environment (120 cores,
  1TB RAM). Estimated runtime 18-24 hours.

(example-twitter)=
## Twitter
Oklobdzija, Stan; Kousser, Thad; Butler, Daniel, 2022, "Replication Data for: Do
Male and Female Legislators Have Different Twitter Communication Styles?",
https://doi.org/10.15139/S3/MHAAZV, UNC Dataverse.
* Uses Twitter data

(example-international-agencies)=
## International statistical agencies

Hjortskov, Morten; Andersen, Simon Calmar; Jakobsen, Morten, 2018, "Replication
Data for: Encouraging Political Voices of Underrepresented Citizens through
Coproduction. Evidence from a Randomized Field Trial". [Replication
package](https://doi.org/10.7910/DVN/MZKJDR)
* Confidential data from Statistics Denmark

Hager, Anselm; Hilbig, Hanno, 2019, "Replication Data for: Do Inheritance
Customs Affect Political and Social Inequality" [Replication
package](https://doi.org/10.7910/DVN/ZUH3UG)
* Confidential data from German SOEP

Bonhomme, Lamadon, and Manresa, forthcoming. "A distributional Framework for
matched employer-employee data". Econometrica. [Github
repo](https://github.com/tlamadon/blm-replicate)
* Docker runs with synthetic data and is designed to run on confidential data
  from Sweden.
* Injecting a bit of code would make this be able to run on Swedish data and 
  demonstrate input data, output results, and possibly some disclosure avoidance 
  review (not specified)


(example-ipums)=
## IPUMS

Jia, Ning, Raven Molloy, Christopher Smith, and Abigail Wozniak. 2023. "The
Economics of Internal Migration: Advances and Policy Questions." Journal of
Economic Literature.
[Paper](https://www.aeaweb.org/articles?id=10.1257/jel.20211623)

* This paper uses [IPUMS USA](caseprofile-ipums) data accessed via API. 
* An [unofficial Github](https://github.com/AEADataEditor/JEL-2021-162) is
  available to demonstrate how the API is used to obtain extracts. A private
  repo provided by the authors has a copy of the extracted data.

