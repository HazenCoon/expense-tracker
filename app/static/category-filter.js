const transactionTypeSelect = document.getElementById("transaction-type");
const categorySelect = document.getElementById("category");
const categoryGroups = Array.from(categorySelect.querySelectorAll("optgroup"));

function updateCategories() {
    const selectedType = transactionTypeSelect.value;
    const matchingGroup = categoryGroups.find(
        (group) => group.dataset.transactionType === selectedType
    );

    categorySelect.replaceChildren(matchingGroup.cloneNode(true));
    categorySelect.selectedIndex = 0;
}

transactionTypeSelect.addEventListener("change", 
    updateCategories
);
updateCategories();