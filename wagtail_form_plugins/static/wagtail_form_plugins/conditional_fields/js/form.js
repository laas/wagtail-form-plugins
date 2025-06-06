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
            .from(dom_input.querySelectorAll('input'))
            .map((dom, index) => [`c${index + 1}`, dom.checked])
            .filter(([i, checked]) => checked)
            .map(([val_id, c]) => val_id);

        return widget === "RadioSelect" ? values[0] : values
    }
    if (["Select", "SelectMultiple"].includes(widget)) {
        const values = Array
            .from(dom_input.querySelectorAll('option'))
            .map((dom, index) => [`c${index + 1}`, dom.selected])
            .filter(([i, selected]) => selected)
            .map(([val_id, c]) => val_id);

        return widget === "Select" ? values[0] : values
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
        const [opr_char, w, opr_func] = OPERATORS[rule.entry.opr]
        const value = get_value(dom_field)

        return {
            formula: `${ dom_field.getAttribute('data-label') } ${ opr_char } "${ rule.entry.val }"`,
            str: `"${ value }" ${ opr_char } "${ rule.entry.val }"`,
            is_active: opr_func(value, rule.entry.val) && dom_field.getAttribute("data-active") !== "n",
            indent_level: parseInt(dom_field.getAttribute("data-level")) + 1,
        }
    }

    if (rule.and) {
        const computed_rules = rule.and.map((_rule) => compute_rule(_rule))
        return {
            formula: `(${ computed_rules.map((_rule) => _rule.formula).join(') AND (') })`,
            str: `(${ computed_rules.map((_rule) => _rule.str).join(') AND (') })`,
            is_active: computed_rules.every((_rule) => _rule.is_active),
            indent_level: Math.max(...computed_rules.map((_rule) => _rule.indent_level)),
        }
    }

    if (rule.or) {
        const computed_rules = rule.or.map((_rule) => compute_rule(_rule))
        return {
            formula: `(${ computed_rules.map((_rule) => _rule.formula).join(') OR (') })`,
            str: `(${ computed_rules.map((_rule) => _rule.str).join(') OR (') })`,
            is_active: computed_rules.some((_rule) => _rule.is_active),
            indent_level: Math.max(...computed_rules.map((_rule) => _rule.is_active ? _rule.indent_level : 0)),
        }
    }

    return {formula: '∅', str: '∅', is_active: true, indent_level: 0}
}

function debounce(callback) {
    let timer;
    return () => {
        clearTimeout(timer);
        timer = setTimeout(() => callback(), DEBOUNCE_DELAY);
    }
}

function update_fields_visibility() {
    console.log('\n===== updating fields visibility =====\n\n')

    for(const dom_field of document.querySelectorAll('form [data-label]')) {
        const rule = JSON.parse(dom_field.getAttribute('data-rule'))
        const computed_rule = compute_rule(rule)
        const dom_input_block = dom_field.getAttribute("data-widget") === "HiddenInput" ? dom_field : dom_field.parentNode

        if (Object.keys(rule).length !== 0) {
            console.log(`\n=== ${ dom_field.getAttribute('data-label') } ===`)
            // console.log('dom_field:', dom_field)
            required_attr = dom_field.getAttributeNode("required")
            if (required_attr !== null) {
                dom_field.removeAttributeNode(required_attr)
            }
            console.log('rule:', rule)
            console.log(`${computed_rule.formula}   ⇒   ${computed_rule.str}   ⇒   ${computed_rule.is_active}`)
        }

        dom_field.setAttribute("data-level", computed_rule.indent_level)
        dom_field.setAttribute("data-active", computed_rule.is_active ? "y" : "n")

        dom_input_block.style.paddingLeft = `${computed_rule.indent_level * 2}em`;
        dom_input_block.style.display = computed_rule.is_active && dom_field ? '' : 'none';
    }
}

document.addEventListener("DOMContentLoaded", () => {
    update_fields_visibility()
    for(const dom_input of document.querySelectorAll('form [data-label]')) {
        dom_input.addEventListener('input', debounce(() => update_fields_visibility()))
    }
});
