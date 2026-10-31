const assert = require("node:assert/strict");

// Sample LocalPro provider applications.
const applications = [
    {
        business_name: "Berkeley Snow Pros",
        contact_name: "John",
        service_area: "Berkeley",
        services: "Snow removal, shoveling, salting",
        status: "approved"
    },
    {
        business_name: "Commercial Ice Solutions",
        contact_name: "Mike",
        service_area: "Elmhurst",
        services: "Commercial snow plowing and ice management",
        status: "pending"
    },
    {
        business_name: "Green Lawn Landscaping",
        contact_name: "Sarah",
        service_area: "Westchester",
        services: "Lawn mowing and landscaping",
        status: "rejected"
    }
];

// Search providers.
function searchApplications(applications, searchText) {
    const search = searchText.trim().toLowerCase();

    return applications.filter(application => {
        const searchableText = [
            application.business_name,
            application.contact_name,
            application.service_area,
            application.services
        ].join(" ").toLowerCase();

        return searchableText.includes(search);
    });
}

// Filter by application status.
function filterByStatus(applications, status) {
    if (status === "all") {
        return applications;
    }

    return applications.filter(
        application => application.status === status
    );
}

// Test snow provider search.
const snowResults = searchApplications(applications, "snow");

assert.equal(snowResults.length, 2);

// Test approved provider filter.
const approvedResults = filterByStatus(applications, "approved");

assert.equal(approvedResults.length, 1);
assert.equal(approvedResults[0].business_name, "Berkeley Snow Pros");

// Test pending provider filter.
const pendingResults = filterByStatus(applications, "pending");

assert.equal(pendingResults.length, 1);

// Test rejected provider filter.
const rejectedResults = filterByStatus(applications, "rejected");

assert.equal(rejectedResults.length, 1);

// Test all applications.
const allResults = filterByStatus(applications, "all");

assert.equal(allResults.length, 3);

// Test application counts.
assert.equal(applications.length, 3);
assert.equal(applications.filter(app => app.status === "approved").length, 1);
assert.equal(applications.filter(app => app.status === "pending").length, 1);
assert.equal(applications.filter(app => app.status === "rejected").length, 1);

console.log("All LocalPro admin dashboard tests passed!");
console.log("Tests completed: 8");