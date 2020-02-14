import * as R from 'ramda';

function setPageIcon(href) {
  let link = document.querySelector("link[rel*='icon']");
  if (!link) {
    link = document.createElement('link');
    document.head.appendChild(link);
  }
  link.type = 'image/x-icon';
  link.rel = 'shortcut icon';
  link.href = href;
}

// hold the icon status from different sources
const sources = {};

export function useWarningIcon(source, warning) {
  sources[source] = warning;
  const warningSources = R.keys(R.filter(v => v, sources));
  const icon = warningSources.length > 0 ? 'favicon-warn.ico' : 'favicon.ico';
  setPageIcon(icon);
}
