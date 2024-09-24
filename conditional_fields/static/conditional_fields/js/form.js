// [label, char, widgets, processing function]
const OPERATORS = {
    'eq': ['is equal to', '=', 'senu', (dom_input, value) => dom_input.value === value],
    'neq': ['is not equal to', '≠', 'senu', (dom_input, value) => dom_input.value !== value],

    'is': ['is', '=', 'lrd', (dom_input, value) => dom_input.value === value],
    'nis': ['is not', '≠', 'lrd', (dom_input, value) => dom_input.value !== value],

    'lt': ['is lower than', '<', 'n', (dom_input, value) => parseFloat(dom_input.value) < parseFloat(value)],
    'lte': ['is lower or equal to', '≤', 'n', (dom_input, value) => parseFloat(dom_input.value) <= parseFloat(value)],

    'ut': ['is upper than', '>', 'n', (dom_input, value) => parseFloat(dom_input.value) > parseFloat(value)],
    'ute': ['is upper or equal to', '≥', 'n', (dom_input, value) => parseFloat(dom_input.value) >= parseFloat(value)],

    'bt': ['is before than', '<', 'dt', (dom_input, value) => Date.parse(dom_input.value) < Date.parse(value)],
    'bte': ['is before or equal to', '≤', 'd', (dom_input, value) => Date.parse(dom_input.value) <= Date.parse(value)],

    'at': ['is after than', '>', 'dt', (dom_input, value) => Date.parse(dom_input.value) > Date.parse(value)],
    'ate': ['is after or equal to', '≥', 'd', (dom_input, value) => Date.parse(dom_input.value) >= Date.parse(value)],

    'ct': ['contains', '∋', 'mCL', (dom_input, value) => dom_input.value.includes(value)],
    'nct': ['does not contain', '∌', 'mCL', (dom_input, value) => ! dom_input.value.includes(value)],

    'c': ['is checked', '✔', 'c', (dom_input, value) => dom_input.checked],
    'nc': ['is not checked', '✖', 'c', (dom_input, value) => !dom_input.checked],
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
            result: opr_func(dom_field, rule.entry.val),
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
    for(const dom_field of document.querySelectorAll('form > p > input.form-control')) {
        const label = dom_field.getAttribute('data-label')
        const rule = JSON.parse(dom_field.getAttribute('data-rule'))
        const cmp_rule = compute_rule(rule)
        console.log(`${label}: ${ cmp_rule.formula }  ⇒  ${ cmp_rule.str }  ⇒  ${ cmp_rule.result }`)

        dom_field.parentNode.style.display = cmp_rule.result ? '' : 'none';
        // dom_field.style.backgroundColor = cmp_rule.result ? '' : 'lightGrey';
    }
}

document.addEventListener("DOMContentLoaded", () => {
    update_fields_visibility()
    Array.from(document.querySelectorAll('input.form-control')).forEach((dom_input) => {
        dom_input.addEventListener('input', debounce(() => update_fields_visibility()))
    });
});
