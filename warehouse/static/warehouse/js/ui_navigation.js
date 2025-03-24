"use strict";

// Show the main menu screen
function showMainMenu() {
  navigationStack = []; // Clear navigation history
  hideAll();
  const mainMenu = document.getElementById('mainMenu');
  if (mainMenu) mainMenu.classList.remove('hidden');
}

// Show the first-level sub-menu for a given category
function showSubMenu(category) {
  navigationStack = [{ type: 'menu', category: category }];
  hideAll();
  const subMenuScreen = document.getElementById('subMenuScreen');
  if (subMenuScreen) subMenuScreen.classList.remove('hidden');
  document.getElementById('subMenuTitle').innerText = category;
  // Set header styling (using header-blue by default)
  document.getElementById('subMenuHeader').className = "header-row header-blue";
  document.getElementById('subMenuContent').innerHTML = getSubMenuContent(category);
}

// Show nested sub-menu options (for further options within a category)
function showNestedSubMenu(mainCategory, parentItem) {
  navigationStack.push({ type: 'nested', mainCategory: mainCategory, parentItem: parentItem });
  hideAll();
  const subMenuScreen = document.getElementById('subMenuScreen');
  if (subMenuScreen) subMenuScreen.classList.remove('hidden');
  document.getElementById('subMenuTitle').innerText = mainCategory + " > " + parentItem;
  document.getElementById('subMenuHeader').className = "header-row header-blue";
  document.getElementById('subMenuContent').innerHTML = getNestedSubMenuContent(mainCategory, parentItem);
}

// Navigate back in the sub-menu screens
function goBackSubMenu() {
  navigationStack.pop();
  if (navigationStack.length === 0) {
    showMainMenu();
  } else {
    const current = navigationStack[navigationStack.length - 1];
    hideAll();
    const subMenuScreen = document.getElementById('subMenuScreen');
    if (subMenuScreen) subMenuScreen.classList.remove('hidden');
    if (current.type === 'menu') {
      document.getElementById('subMenuTitle').innerText = current.category;
      document.getElementById('subMenuContent').innerHTML = getSubMenuContent(current.category);
    } else if (current.type === 'nested') {
      document.getElementById('subMenuTitle').innerText = current.mainCategory + " > " + current.parentItem;
      document.getElementById('subMenuContent').innerHTML = getNestedSubMenuContent(current.mainCategory, current.parentItem);
    }
  }
}

// Return from workflow detail screen to the current sub-menu
function returnToSubMenu() {
  hideAll();
  const subMenuScreen = document.getElementById('subMenuScreen');
  if (subMenuScreen) subMenuScreen.classList.remove('hidden');
}

// Show the workflow detail screen for a selected item
function showWorkflowItem(mainCategory, item) {
  hideAll();
  const workflowScreen = document.getElementById('workflowScreen');
  if (workflowScreen) workflowScreen.classList.remove('hidden');
  document.getElementById('workflowTitle').innerText = mainCategory + " - " + item;
  document.getElementById('workflowContent').innerHTML = getWorkflowContent(mainCategory, item);
  const scannerInput = document.getElementById('scannerInput');
  if (scannerInput) scannerInput.focus();
}

/* Dummy functions to return HTML content.
   Replace these with your real API-driven content as needed. */
function getSubMenuContent(category) {
  let content = '';
  if (category === 'Receive') {
    content = `
      <div class="col-12 col-md-4">
        <div class="card menu-card" onclick="showWorkflowItem('Receive', 'New Inventory')">
          <div class="card-body">
            <span class="icon-circle icon-blue"><i class="fas fa-file-alt"></i></span>
            1.1 New Inventory
          </div>
        </div>
      </div>
      <div class="col-12 col-md-4">
        <div class="card menu-card" onclick="showWorkflowItem('Receive', 'Returns')">
          <div class="card-body">
            <span class="icon-circle icon-blue"><i class="fas fa-undo"></i></span>
            1.2 Returns
          </div>
        </div>
      </div>
      <div class="col-12 col-md-4">
        <div class="card menu-card" onclick="showWorkflowItem('Receive', 'Cross-dock')">
          <div class="card-body">
            <span class="icon-circle icon-blue"><i class="fas fa-exchange-alt"></i></span>
            1.3 Cross-dock
          </div>
        </div>
      </div>
      <div class="col-12 col-md-4">
        <div class="card menu-card" onclick="showWorkflowItem('Receive', 'Put in stock')">
          <div class="card-body">
            <span class="icon-circle icon-blue"><i class="fas fa-store"></i></span>
            1.4 Put in stock
          </div>
        </div>
      </div>
    `;
  }
  // Add content for other categories as needed.
  return content;
}

function getNestedSubMenuContent(mainCategory, parentItem) {
  // Return nested submenu HTML based on parameters.
  return '';
}

function getWorkflowContent(category, item) {
  let instructions = '<ol>';
  if (category === 'Receive' && item === 'New Inventory') {
    instructions += `
      <li>Call /receiveInventory/ API to fetch inventory items.</li>
      <li>Select an item and scan the inbound staging area.</li>
      <li>Send notification to update MovementHistory.</li>
      <li>Display message in green: "reference_id moved to location_id".</li>
      <li>Restart step 1.1.</li>
    `;
  }
  // Add other workflows as needed.
  instructions += '</ol><p>Note: The scan input field below is always active for immediate processing.</p>';
  return instructions;
}

// Expose functions to global scope
window.showMainMenu = showMainMenu;
window.showSubMenu = showSubMenu;
window.showNestedSubMenu = showNestedSubMenu;
window.goBackSubMenu = goBackSubMenu;
window.returnToSubMenu = returnToSubMenu;
window.showWorkflowItem = showWorkflowItem;