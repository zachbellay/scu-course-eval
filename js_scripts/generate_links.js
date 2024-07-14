import authenticate from "./get_auth_tokens.js";
import dotenv from "dotenv";
import jsdom from "jsdom";
import fs from "fs";

dotenv.config();

const LOGIN_TITLE = "<title>SCU Login";
const EVALUATIONS_URL = "https://www.scu.edu/apps/evaluations/";
const REQUEST_INTERVAL_MS = 500;

let authTokens = await authenticate(
  process.env.SCU_USERNAME,
  process.env.SCU_PASSWORD
);

async function generateAllPdfLinks() {
  const schoolsAndTerms = await getSchoolsAndTerms();
  let pdfLinks = new Set();
  for (const term of schoolsAndTerms.terms) {
    let queryResultsDoc = await fetchWithAuth(generateSearchLink(term));
    if (shouldIncreaseSearchGranularity(queryResultsDoc)) {
      console.log(`Using school granularity for term ${term}`);
      for (const school of schoolsAndTerms.schools) {
        queryResultsDoc = await fetchWithAuth(generateSearchLink(term, school));
        if (shouldIncreaseSearchGranularity(queryResultsDoc)) {
          console.log(
            `Using letter granularity for school ${school} on term ${term}`
          );
          for (let i = 0; i < 26; i++) {
            queryResultsDoc = await fetchWithAuth(
              generateSearchLink(term, school, String.fromCharCode(97 + i))
            );
            addLinksFromQueryResults(queryResultsDoc, pdfLinks);
          }
        }
        addLinksFromQueryResults(queryResultsDoc, pdfLinks);
      }
    }
    console.log(`Finished getting links for term: ${term}`);
    addLinksFromQueryResults(queryResultsDoc, pdfLinks);
    // Links from each term are unique, so we can update the file now.
    writeToLinksFile(pdfLinks, term);
  }
}

function addLinksFromQueryResults(queryResultsDoc, pdfLinks) {
  const resultLinks = queryResultsDoc.querySelectorAll("tr>td>a");
  for (let link of resultLinks) {
    if (link.href && link.href.trim())
      pdfLinks.add(`${EVALUATIONS_URL}${link.href}`);
  }
}

function writeToLinksFile(pdfLinks) {
  fs.writeFileSync("pdf_links.txt", "");
  const linksFile = fs.createWriteStream("pdf_links.txt", { flags: "a" });
  for (let link of pdfLinks) {
    linksFile.write(`${link}\n`);
  }
  linksFile.end();
}

async function getSchoolsAndTerms() {
  const doc = await fetchWithAuth(EVALUATIONS_URL);
  const schoolElements = doc.querySelector("#school").children;
  let schools = [];
  for (let el of schoolElements) {
    if (el.value.trim() === "") {
      continue;
    } else schools.push(el.value.trim());
  }
  let termElements = doc.querySelector("#term").children;
  let terms = [];
  for (let el of termElements) {
    if (el.value.trim() === "") {
      continue;
    } else if (
      parseInt(el.value.trim()) >= 3040 ||
      isNaN(parseInt(el.value.trim()))
    ) {
      terms.push(el.value.trim());
    }
  }
  console.log(`Got schools: ${schools}`);
  console.log(`Got terms: ${terms}`);
  return { schools, terms };
}

function generateSearchLink(term, school = "", searchQuery = "") {
  return `${EVALUATIONS_URL}?ds=1&searchq=${searchQuery}&ds=2&term=${term}&school=${school}&faculty=&course=`;
}

function shouldIncreaseSearchGranularity(htmlDoc) {
  return htmlDoc.querySelector("#maxResultExceeded") !== null;
}

async function fetchWithAuth(url, isPdfRequest = false) {
  // Wait to prevent accidental DDoS.
  await new Promise((resolve) => setTimeout(resolve, REQUEST_INTERVAL_MS));
  if (isPdfRequest) {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        Cookie: `SimpleSAML=${authTokens.SimpleSAML}; SimpleSAMLAuthToken=${authTokens.SimpleSAMLAuthToken}`,
      },
    });
    if (badAuthForPdfRequest(response)) {
      authTokens = await authenticate();
      return fetchWithAuth(url, isPdfRequest);
    }
  } else {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        Cookie: `SimpleSAML=${authTokens.SimpleSAML}; SimpleSAMLAuthToken=${authTokens.SimpleSAMLAuthToken}`,
      },
    });
    const responseText = await response.text();
    if (badAuthForQueryRequest(responseText)) {
      authTokens = await authenticate();
      return fetchWithAuth(url, isPdfRequest);
    }
    return new jsdom.JSDOM(responseText).window.document;
  }
}

function badAuthForQueryRequest(htmlResponse) {
  if (htmlResponse.includes(LOGIN_TITLE)) {
    console.log("Auth expired. Reauthenticating...");
    authenticate();
    return true;
  }
  return false;
}

function badAuthForPdfRequest(response) {
  if (response.headers.get("Content-Type") !== "application/pdf") {
    console.log("Auth expired. Reauthenticating...");
    authenticate();
    return true;
  }
  return false;
}

generateAllPdfLinks();
