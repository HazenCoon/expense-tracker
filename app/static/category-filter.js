const transactionTypeInputs = document.querySelectorAll('input[name="transaction_type"]');
const categorySelect = document.getElementById("category");
const categoryGroups = Array.from(categorySelect.querySelectorAll("optgroup"));

function updateCategories() {
    const selectedType = document.querySelector('input[name="transaction_type"]:checked').value;
    const matchingGroup = categoryGroups.find(
        (group) => group.dataset.transactionType === selectedType
    );

    categorySelect.replaceChildren(matchingGroup.cloneNode(true));
    categorySelect.selectedIndex = 0;
}

transactionTypeInputs.forEach((input) => {
    input.addEventListener("change", updateCategories);
});
updateCategories();
