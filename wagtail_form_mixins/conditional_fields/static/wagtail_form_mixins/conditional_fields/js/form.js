function get_value(dom_input) {
    const widget = dom_input.getAttribute('data-widget')
    if (widget === "NumberInput") {
        return parseFloat(dom_input.value)
    }
    if (widget === "CheckboxInput") {
        return dom_input.checked
    }
    if (["CheckboxSelectMultiple", "RadioSelect"].includes(widget)) {
        const values = Array
            .from(dom_input.closest('div[id]').querySelectorAll('input'))
            .map((dom, index) => [`c${index + 1}`, dom.checked])
            .filter(([i, checked]) => checked)
            .map(([val_id, c]) => val_id);

        return widget === "RadioSelect" ? values[0] : values
    }
    if (["DateInput", "DateTimeInput"].includes(widget)) {
        return Date.parse(dom_input.value)
    }
    return dom_input.value
}

// [label, char, widgets, processing function]
const OPERATORS = {
    'eq': ['=', 'senu', (a, b) => a === b],
    'neq': ['≠', 'senu', (a, b) => a !== b],

    'is': ['=', 'lrd', (a, b) => a === b],
    'nis': ['≠', 'lrd', (a, b) => a !== b],

    'lt': ['<', 'n', (a, b) => a < parseFloat(b)],
    'lte': ['≤', 'n', (a, b) => a <= parseFloat(b)],

    'ut': ['>', 'n', (a, b) => a > parseFloat(b)],
    'ute': ['≥', 'n', (a, b) => a >= parseFloat(b)],

    'bt': ['<', 'dt', (a, b) => a < Date.parse(b)],
    'bte': ['≤', 'd', (a, b) => a <= Date.parse(b)],

    'at': ['>', 'dt', (a, b) => a > Date.parse(b)],
    'ate': ['≥', 'd', (a, b) => a >= Date.parse(b)],

    'ct': ['∋', 'mCL', (a, b) => a.includes(b)],
    'nct': ['∌', 'mCL', (a, b) => ! a.includes(b)],

    'c': ['✔', 'c', (a, b) => a],
    'nc': ['✖', 'c', (a, b) => !a],
}
const DEBOUNCE_DELAY = 300;


function compute_rule(rule) {
    if (rule.entry) {
        let dom_field = document.getElementById(rule.entry.target)
        const [char, w, opr_func] = OPERATORS[rule.entry.opr]

        if (dom_field.nodeName === 'DIV') {
            dom_field = dom_field.querySelector('input')
        }

        return {
            formula: `${ dom_field.getAttribute('data-label') } ${ char } "${ rule.entry.val }"`,
            str: `"${ dom_field.value }" ${ char } "${ rule.entry.val }"`,
            result: opr_func(get_value(dom_field), rule.entry.val),
        }
    }

    if (rule.and) {
        const computed_rules = rule.and.map((_rule) => compute_rule(_rule))
        return {
            formula: `(${ computed_rules.map((_rule) => _rule.formula).join(') AND (') })`,
            str: `(${ computed_rules.map((_rule) => _rule.str).join(') AND (') })`,
            result: computed_rules.every((_rule) => _rule.result),
        }
    }

    if (rule.or) {
        const computed_rules = rule.or.map((_rule) => compute_rule(_rule))
        return {
            formula: `(${ computed_rules.map((_rule) => _rule.formula).join(') OR (') })`,
            str: `(${ computed_rules.map((_rule) => _rule.str).join(') OR (') })`,
            result: computed_rules.some((_rule) => _rule.result),
        }
    }

    return {formula: '∅', str: '∅', result: true}
}

function debounce(callback) {
    let timer;
    return () => {
        clearTimeout(timer);
        timer = setTimeout(() => callback(), DEBOUNCE_DELAY);
    }
}

function update_fields_visibility() {
    console.clear()
    for(const dom_field of document.querySelectorAll('form [data-label]')) {
        const rule = JSON.parse(dom_field.getAttribute('data-rule'))
        const cmp_rule = compute_rule(rule)

        if (Object.keys(rule).length !== 0) {
            console.log(`\n=== ${ dom_field.getAttribute('data-label') } ===`)
            // console.log('dom_field:', dom_field)
            console.log('rule:', rule)
            console.log(`${cmp_rule.formula}  ⇒  ${cmp_rule.str}  ⇒  ${cmp_rule.result}`)
        }

        dom_field.parentNode.style.display = cmp_rule.result ? '' : 'none';
    }
}

document.addEventListener("DOMContentLoaded", () => {
    update_fields_visibility()
    for(const dom_input of document.querySelectorAll('form [data-label]')) {
        dom_input.addEventListener('input', debounce(() => update_fields_visibility()))
    }
});
