function get_value(dom_input) {
    const widget = dom_input.getAttribute('data-widget')
    if (widget === "NumberInput") {
        return parseFloat(dom_input.value)
    }
    if (widget === "CheckboxInput") {
        return dom_input.checked
    }
    if (["CheckboxSelectMultiple", "RadioSelect"].includes(widget)) {
        const dom_inputs = dom_input.closest('div.form-control').querySelectorAll('input.form-control:checked')
        const values = Array.from(dom_inputs).map((_dom_input) => _dom_input.value)
        return widget === "RadioSelect" ? values[0] : values
    }
    if (["DateInput", "DateTimeInput"].includes(widget)) {
        return Date.parse(dom_input.value)
    }
    return dom_input.value
}

// [label, char, widgets, processing function]
const OPERATORS = {
    'eq': ['is equal to', '=', 'senu', (a, b) => a.value === b],
    'neq': ['is not equal to', '≠', 'senu', (a, b) => a.value !== b],

    'is': ['is', '=', 'lrd', (a, b) => a === b],
    'nis': ['is not', '≠', 'lrd', (a, b) => a !== b],

    'lt': ['is lower than', '<', 'n', (a, b) => a < parseFloat(b)],
    'lte': ['is lower or equal to', '≤', 'n', (a, b) => a <= parseFloat(b)],

    'ut': ['is upper than', '>', 'n', (a, b) => a > parseFloat(b)],
    'ute': ['is upper or equal to', '≥', 'n', (a, b) => a >= parseFloat(b)],

    'bt': ['is before than', '<', 'dt', (a, b) => a < Date.parse(b)],
    'bte': ['is before or equal to', '≤', 'd', (a, b) => a <= Date.parse(b)],

    'at': ['is after than', '>', 'dt', (a, b) => a > Date.parse(b)],
    'ate': ['is after or equal to', '≥', 'd', (a, b) => a >= Date.parse(b)],

    'ct': ['contains', '∋', 'mCL', (a, b) => a.includes(b)],
    'nct': ['does not contain', '∌', 'mCL', (a, b) => ! a.includes(b)],

    'c': ['is checked', '✔', 'c', (a, b) => a],
    'nc': ['is not checked', '✖', 'c', (a, b) => !a],
}
const DEBOUNCE_DELAY = 300;


function compute_rule(rule) {
    if (rule.entry) {
        let dom_field = document.getElementById(rule.entry.target)
        const [opr_str, c, w, opr_func] = OPERATORS[rule.entry.opr]

        if (dom_field.nodeName === 'DIV') {
            dom_field = dom_field.querySelector('input')
        }

        return {
            formula: `${ dom_field.getAttribute('data-label') } ${ opr_str } "${ rule.entry.val }"`,
            str: `"${ dom_field.value }" ${ opr_str } "${ rule.entry.val }"`,
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
    // console.clear()
    for(const dom_field of document.querySelectorAll('form > p > input.form-control')) {
        const rule = JSON.parse(dom_field.getAttribute('data-rule'))
        const cmp_rule = compute_rule(rule)
        // console.log(`${dom_field.getAttribute('data-label')}: ${cmp_rule.formula}  ⇒  ${cmp_rule.str}  ⇒  ${cmp_rule.result}`)

        dom_field.parentNode.style.display = cmp_rule.result ? '' : 'none';
        // dom_field.style.backgroundColor = cmp_rule.result ? '' : 'lightGrey';
    }
}

document.addEventListener("DOMContentLoaded", () => {
    update_fields_visibility()
    Array.from(document.querySelectorAll('.form-control')).forEach((dom_input) => {
        dom_input.addEventListener('input', debounce(() => update_fields_visibility()))
    });
});
