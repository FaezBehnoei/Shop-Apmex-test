import { boot } from 'quasar/wrappers'

const persianDigits = '۰۱۲۳۴۵۶۷۸۹'
const toPersianNum = str =>
  str.replace(/\d/g, d => persianDigits[d])

function convertTextNodes(root) {
  const walker = document.createTreeWalker(
    root,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode: node =>
        /\d/.test(node.nodeValue)
          ? NodeFilter.FILTER_ACCEPT
          : NodeFilter.FILTER_REJECT
    },
    false
  )
  let node
  while ((node = walker.nextNode())) {
    node.nodeValue = toPersianNum(node.nodeValue)
  }
}

function convertInputs(root) {
  const inputs = root.querySelectorAll('input:not([data-no-fa]), textarea:not([data-no-fa])')
  for (const input of inputs) {
    // فقط برای نوع‌هایی که از selectionRange پشتیبانی می‌کنن
    const validTypes = ['text', 'tel', 'number', 'password', 'search']
    if (input.tagName === 'TEXTAREA' || validTypes.includes(input.type)) {
      input.addEventListener('input', () => {
        const start = input.selectionStart
        const end = input.selectionEnd
        input.value = toPersianNum(input.value)
        input.setSelectionRange(start, end)
      })

      // در صورت لود اولیه با مقدار
      input.value = toPersianNum(input.value)
    }
  }
}

function setupObserver(root) {
  const observer = new MutationObserver(mutations => {
    for (const m of mutations) {
      for (const node of m.addedNodes) {
        if (node.nodeType === Node.ELEMENT_NODE) {
          convertTextNodes(node)
          convertInputs(node)
        } else if (node.nodeType === Node.TEXT_NODE) {
          node.nodeValue = toPersianNum(node.nodeValue)
        }
      }
    }
  })

  observer.observe(root, {
    childList: true,
    subtree: true,
    characterData: true
  })
}

export default boot(() => {
  const root = document.getElementById('q-app') || document.body
  if (root) {
    convertTextNodes(root)
    convertInputs(root)
    setupObserver(root)
  }
})
