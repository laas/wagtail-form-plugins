function get_value(dom_input) {
	const field_type = dom_input.getAttribute("data-type");
	if (field_type === "number") {
		return parseFloat(dom_input.value);
	}
	if (field_type === "checkbox") {
		return dom_input.checked;
	}
	if (["checkboxes", "radio"].includes(field_type)) {
		const values = Array.from(dom_input.querySelectorAll("input"))
			.map((dom, index) => [`c${index + 1}`, dom.checked])
			.filter(([_index, checked]) => checked)
			.map(([val_id, _checked]) => val_id);

		return field_type === "radio" ? values[0] : values;
	}
	if (["dropdown", "multiselect"].includes(field_type)) {
		const values = Array.from(dom_input.querySelectorAll("option"))
			.map((dom, index) => [`c${index + 1}`, dom.selected])
			.filter(([_index, selected]) => selected)
			.map(([val_id, _selected]) => val_id);

		return field_type === "dropdown" ? values[0] : values;
	}
	if (["date", "time", "datetime"].includes(field_type)) {
		const date = Date.parse((field_type === "time" ? "1970-01-01T" : "") + dom_input.value);
		return Math.floor(date / 1000);
	}
	return dom_input.value;
}

// [char, widgets, processing function]
const OPERATORS = {
	eq: ["=", "senu", (a, b) => a === b],
	neq: ["≠", "senu", (a, b) => a !== b],

	is: ["=", "lrd", (a, b) => a === b],
	nis: ["≠", "lrd", (a, b) => a !== b],

	lt: ["<", "n", (a, b) => a < b],
	lte: ["≤", "n", (a, b) => a <= b],

	ut: [">", "n", (a, b) => a > b],
	ute: ["≥", "n", (a, b) => a >= b],

	bt: ["<", "dt", (a, b) => a < b],
	bte: ["≤", "d", (a, b) => a <= b],

	at: [">", "dt", (a, b) => a > b],
	ate: ["≥", "d", (a, b) => a >= b],

	ct: ["∋", "mCL", (a, b) => a.includes(b)],
	nct: ["∌", "mCL", (a, b) => !a.includes(b)],

	c: ["✔", "c", (a, _b) => a],
	nc: ["✖", "c", (a, _b) => !a],
};
const DEBOUNCE_DELAY = 300;

function compute_rule(rule) {
	if (rule.entry) {
		const dom_field = document.getElementById(rule.entry.target);
		const [opr_char, _widgets, opr_func] = OPERATORS[rule.entry.opr];
		const value = get_value(dom_field);

		return {
			formula: `${dom_field.getAttribute("data-label")} ${opr_char} ${rule.entry.val}`,
			str: `${value} ${opr_char} ${rule.entry.val}`,
			is_active:
				opr_func(value, rule.entry.val) && dom_field.getAttribute("data-active") !== "n",
			indent_level: parseInt(dom_field.getAttribute("data-level"), 10) + 1,
		};
	}

	if (rule?.bool_opr === "and") {
		const computed_rules = rule.subrules.map((_rule) => compute_rule(_rule));
		return {
			formula: `(${computed_rules.map((_rule) => _rule.formula).join(") AND (")})`,
			str: `(${computed_rules.map((_rule) => _rule.str).join(") AND (")})`,
			is_active: computed_rules.every((_rule) => _rule.is_active),
			indent_level: Math.max(...computed_rules.map((_rule) => _rule.indent_level)),
		};
	}

	if (rule?.bool_opr === "or") {
		const computed_rules = rule.subrules.map((_rule) => compute_rule(_rule));
		return {
			formula: `(${computed_rules.map((_rule) => _rule.formula).join(") OR (")})`,
			str: `(${computed_rules.map((_rule) => _rule.str).join(") OR (")})`,
			is_active: computed_rules.some((_rule) => _rule.is_active),
			indent_level: Math.max(
				...computed_rules.map((_rule) => (_rule.is_active ? _rule.indent_level : 0)),
			),
		};
	}

	return { formula: "∅", str: "∅", is_active: true, indent_level: 0 };
}

function debounce(callback) {
	let timer;
	return () => {
		clearTimeout(timer);
		timer = setTimeout(() => callback(), DEBOUNCE_DELAY);
	};
}

function update_fields_visibility() {
	console.log("\n===== updating fields visibility =====\n\n");

	for (const dom_field of document.querySelectorAll("form [data-rule]")) {
		const rule = JSON.parse(dom_field.getAttribute("data-rule"));
		const computed_rule = compute_rule(rule);
		const dom_input_block =
			dom_field.getAttribute("data-widget") === "hidden" ? dom_field : dom_field.parentNode;

		if (Object.keys(rule).length !== 0) {
			console.log(`\n=== ${dom_field.getAttribute("data-label")} ===`);
			// console.log('dom_field:', dom_field)
			required_attr = dom_field.getAttributeNode("required");
			if (required_attr !== null) {
				dom_field.removeAttributeNode(required_attr);
			}
			console.log("rule:", rule);
			console.log(
				`${computed_rule.formula}   ⇒   ${computed_rule.str}   ⇒   ${computed_rule.is_active}`,
			);
		}

		dom_field.setAttribute("data-level", computed_rule.indent_level);
		dom_field.setAttribute("data-active", computed_rule.is_active ? "y" : "n");

		dom_input_block.style.paddingLeft = `${computed_rule.indent_level * 2}em`;
		dom_input_block.style.display = computed_rule.is_active && dom_field ? "" : "none";
	}
}

function set_required_attributes(dom_input) {
	if (dom_input.hasAttribute("required")) {
		if (dom_input.getAttribute("data-type") === "radio") {
			for (const dom_input_option of dom_input.querySelectorAll("input")) {
				dom_input_option.setAttribute("required", "");
			}
		} else if (dom_input.getAttribute("data-type") === "checkboxes") {
			for (const dom_input_option of dom_input.querySelectorAll("input")) {
				dom_input_option.setAttribute("required", "");
				dom_input_option.addEventListener("change", (_event) => {
					const one_input_is_checked = [...dom_input.querySelectorAll("input")]
						.map((i) => i.checked)
						.some((checked) => checked);
					for (const _dom_input_option of dom_input.querySelectorAll("input")) {
						if (one_input_is_checked) {
							_dom_input_option.removeAttribute("required");
						} else {
							_dom_input_option.setAttribute("required", "");
						}
					}
				});
			}
		}
	}
}

document.addEventListener("DOMContentLoaded", () => {
	update_fields_visibility();
	for (const dom_input of document.querySelectorAll("form [data-label]")) {
		dom_input.addEventListener(
			"input",
			debounce(() => update_fields_visibility()),
		);
		set_required_attributes(dom_input);
	}
});
