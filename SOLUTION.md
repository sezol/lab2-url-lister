# Lab 2 - UrlCount Solution

## Approach

I converted the WordCount example into UrlCount using the Hadoop Streaming API with Python.

- URLmapper.py: Reads input line by line, uses a regular expression (href="([^"]*)") to find all URLs referenced via href attributes, and emits each URL with a count of 1 (url TAB 1).
- URLreducer.py: Reads the sorted mapper output, sums counts per URL (since Hadoop guarantees identical keys arrive consecutively after sorting), and only prints URLs whose total count is greater than 5.

## Software / Environment

- Hadoop 3.3.6 (Hadoop Streaming API)
- Python 3
- Tested first on the course Coding environment (coding.csel.io), then on Google Cloud Dataproc.
- Dataproc cluster created with gcloud dataproc clusters create, using Google Cloud Skills Boost credits (temporary qwiklabs-gcp project), region europe-west4.

## Resources Used

- Course Hadoop tutorial and Lab 2 instructions
- Google Cloud Dataproc documentation
- Google Cloud Skills Boost lab "Dataproc: Qwik Start - Command Line" (GSP104) to learn the gcloud dataproc command line workflow
- Course Piazza thread for help with a Dataproc permissions error (had to grant storage.admin role to the default compute service account)
- Used Claude (AI assistant) occasionally for help debugging setup issues and understanding some of the gcloud/Hadoop error messages

## Collaboration

I worked on this assignment on my own.

## Results

Output format: URL, tab, count -- for all URLs referenced via href="..." that appear more than 5 times across both input Wikipedia articles (Apache_Hadoop and MapReduce pages).

Sample output:

    #	18
    https://en.wikipedia.org/wiki/Google_File_System	6
    https://en.wikipedia.org/wiki/ISBN_(identifier)	18
    https://en.wikipedia.org/wiki/S2CID_(identifier)	14
    mw-data:TemplateStyles:r1295599781	33
    mw-data:TemplateStyles:r886049734	12
    https://en.wikipedia.org/wiki/Doi_(identifier)	18
    https://en.wikipedia.org/wiki/MapReduce	6
    mw-data:TemplateStyles:r1333133064	7
    mw-data:TemplateStyles:r1333433106	121

## Timing Comparison: 2 Workers vs 4 Workers

Both runs used the same cluster (test-dataproc, e2-standard-2 master and workers, region europe-west4), same input data, and the same mapper/reducer code, run using time make urlstream.

| Configuration | Real time  | User time |
|---------------|-----------|-----------|
| 2 workers     | 1m37.151s | 0m24.028s |
| 4 workers     | 1m12.761s | 0m24.692s |

Both runs produced the exact same output (same 10 URLs, same counts), which makes sense since changing the number of workers should only affect performance, not correctness.

## Discussion

Going from 2 to 4 workers cut the runtime by about 25%, from around 97 seconds down to 73 seconds. I expected it to be closer to twice as fast since we doubled the number of workers, but it wasn't. My guess is that this is because the input data is pretty small (two Wikipedia pages, under 1MB combined), so a lot of the total time is fixed overhead that doesn't get faster just by adding workers -- things like the cluster starting up the job, YARN scheduling tasks, and the shuffle/sort step between the mappers and reducers. There were only 10 input splits being processed, so extra workers mostly just meant less waiting around for a split to free up, not more actual parallel work happening. I'd expect adding workers to help a lot more if the input files were much bigger.
