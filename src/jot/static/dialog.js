// Fallback for browsers without invoker commands: open `command="show-modal"` dialogs on click
if (!("commandForElement" in HTMLButtonElement.prototype)) {
  document.addEventListener("click", (event) => {
    const button = event.target.closest('button[command="show-modal"][commandfor]');
    const dialog = button && document.getElementById(button.getAttribute("commandfor"));
    if (dialog instanceof HTMLDialogElement) dialog.showModal();
  });
}
