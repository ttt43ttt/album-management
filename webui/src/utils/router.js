let history;

export function _setHistory(theHistory) {
  history = theHistory;
}

function push() {
  history.push(...arguments);
}

function replace() {
  history.replace(...arguments);
}

export default { push, replace };
