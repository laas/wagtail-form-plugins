// [label, char, widgets, processing function]
// Labels should be consistent with OPERATIONS dict in wagtail_form_plugins/conditional_fields/models.py
const OPERATORS = {
	eq: ["=", "senu", (a, b) => a.value === b],
	neq: ["≠", "senu", (a, b) => a.value !== b],

	is: ["=", "lrdtD", (a, b) => a === b],
	nis: ["≠", "lrdtD", (a, b) => a !== b],

	lt: ["<", "n", (a, b) => a < parseFloat(b)],
	lte: ["≤", "n", (a, b) => a <= parseFloat(b)],

	ut: [">", "n", (a, b) => a > parseFloat(b)],
	ute: ["≥", "n", (a, b) => a >= parseFloat(b)],

	bt: ["<", "dtD", (a, b) => a < Date.parse(b)],
	bte: ["≤", "dtD", (a, b) => a <= Date.parse(b)],

	at: [">", "dtD", (a, b) => a > Date.parse(b)],
	ate: ["≥", "dtD", (a, b) => a >= Date.parse(b)],

	ct: ["∋", "mCL", (a, b) => a.includes(b)],
	nct: ["∌", "mCL", (a, b) => !a.includes(b)],

	c: ["✔", "c", (a, _b) => a],
	nc: ["✖", "c", (a, _b) => !a],
};

// [field type identifier, widget type]
const FIELD_CUSTOMIZATION = {
	singleline: ["s", "char"],
	multiline: ["m", "char"],
	email: ["e", "char"],
	number: ["n", "number"],
	url: ["u", "char"],
	checkbox: ["c", "none"],
	checkboxes: ["C", "dropdown"],
	dropdown: ["l", "dropdown"],
	multiselect: ["L", "dropdown"],
	radio: ["r", "dropdown"],
	date: ["d", "date"],
	time: ["t", "time"],
	datetime: ["D", "datetime"],
	hidden: ["h", "char"],
	file: ["f", "none"],
	label: ["b", "none"],
};

function get_fields() {
	const dom_form_fields = document.querySelector(".formbuilder-fields-block > div");
	const dom_block_fields = dom_form_fields.querySelectorAll(
		":scope > [data-contentpath]:not([aria-hidden])",
	);

	return Object.fromEntries(
		Array.from(dom_block_fields).map((dom_block, index) => [
			dom_block.getAttribute("data-contentpath"),
			{
				index: index,
				contentpath: dom_block.getAttribute("data-contentpath"),
				label:
					dom_block.querySelector(".formbuilder-field-block-label input").value ||
					`field n°${index + 1}`,
				dom_block: dom_block,
				type: Array.from(dom_block.querySelector(".formbuilder-field-block").classList)
					.find((classname) => classname.startsWith("formbuilder-field-block-"))
					.split("-")[3],
			},
		]),
	);
}

function get_value_choices(selected_field) {
	return selected_field.dom_block
		.querySelector("[data-contentpath=choices] textarea")
		.value.split("\n")
		.map((dom_label, index) => [`c${index + 1}`, dom_label]);
}

function get_field_choices(fields, field_index) {
	return [
		[undefined, "<Select field>", false],
		["", "Fields:", true],
		...Object.values(fields)
			.filter((f) => field_index > f.index)
			.filter((f) => !["hidden", "label", "file"].includes(f.type))
			.map((f) => [f.contentpath, f.label, false]),
		["", "Expression:", true],
		["or", "one of...", false],
		["and", "all of...", false],
	];
}

function on_rule_subject_selected(dom_dropdown) {
	const dom_beb = dom_dropdown.closest(".formbuilder-beb");

	const dom_input_field_id = dom_beb.querySelector(".formbuilder-beb-field > div > input");
	dom_input_field_id.value = dom_dropdown.value;

	const dom_operator = dom_beb.querySelector("div:has(> div > .formbuilder-beb-operator)");
	const dom_val_char = dom_beb.querySelector("div:has(> div > .formbuilder-beb-val-char)");
	const dom_val_num = dom_beb.querySelector("div:has(> div > .formbuilder-beb-val-num)");
	const dom_val_list = dom_beb.querySelector("div:has(> div > .formbuilder-beb-val-list)");
	const dom_val_date = dom_beb.querySelector("div:has(> div > .formbuilder-beb-val-date)");
	const dom_val_time = dom_beb.querySelector("div:has(> div > .formbuilder-beb-val-time)");
	const dom_val_datetime = dom_beb.querySelector(
		"div:has(> div > .formbuilder-beb-val-datetime)",
	);
	const dom_rules = dom_beb.querySelector("div:has(> .formbuilder-beb-rules)");

	if (["and", "or"].includes(dom_dropdown.value)) {
		dom_operator.classList.toggle("formbuilder-hide", true);
		dom_val_char.classList.toggle("formbuilder-hide", true);
		dom_val_num.classList.toggle("formbuilder-hide", true);
		dom_val_list.classList.toggle("formbuilder-hide", true);
		dom_val_date.classList.toggle("formbuilder-hide", true);
		dom_val_time.classList.toggle("formbuilder-hide", true);
		dom_val_datetime.classList.toggle("formbuilder-hide", true);
		dom_rules.classList.toggle("formbuilder-hide", false);
	} else {
		const selected_field = get_fields()[dom_dropdown.value];
		const dom_operator_select = dom_operator.querySelector("select");
		let [field_type_id, widget_type] = [undefined, undefined];

		if (selected_field === undefined) {
			dom_operator_select.setAttribute("disabled", "");
		} else {
			dom_operator_select.removeAttribute("disabled");
			[field_type_id, widget_type] = FIELD_CUSTOMIZATION[selected_field.type];
		}

		dom_operator.classList.toggle("formbuilder-hide", false);
		dom_val_char.classList.toggle("formbuilder-hide", widget_type !== "char");
		dom_val_num.classList.toggle("formbuilder-hide", widget_type !== "number");
		dom_val_list.classList.toggle("formbuilder-hide", widget_type !== "dropdown");
		dom_val_date.classList.toggle("formbuilder-hide", widget_type !== "date");
		dom_val_time.classList.toggle("formbuilder-hide", widget_type !== "time");
		dom_val_datetime.classList.toggle("formbuilder-hide", widget_type !== "datetime");
		if (dom_rules !== undefined && dom_rules !== null) {
			dom_rules.classList.toggle("formbuilder-hide", true);
		}

		const operators = Object.entries(OPERATORS)
			.filter(([_i, [_c, opr_widgets, _f]]) => opr_widgets.includes(field_type_id))
			.map(([opr_id, _cwf]) => opr_id);

		for (dom_option of dom_operator.querySelectorAll("select > option")) {
			dom_option.classList.toggle("formbuilder-hide", !operators.includes(dom_option.value));
		}

		if (widget_type === "dropdown") {
			const dom_val_list_input = dom_val_list.querySelector("input");
			const dom_dropdown = build_virtual_dropdown(
				dom_val_list_input,
				get_value_choices(selected_field),
			);
			dom_val_list_input.value = dom_dropdown.value;
		}
	}

	const visibleOption = dom_operator.querySelector("select option:not(.formbuilder-hide)");
	if (
		visibleOption &&
		!dom_operator.querySelector("select option:not(.formbuilder-hide):checked")
	) {
		visibleOption.selected = true;
	}
}

function build_virtual_dropdown(dom_input, choices) {
	let dom_dropdown = dom_input.parentNode.querySelector("select");
	const selection = dom_input.value || choices.find(([_k, _s, disabled]) => !disabled)[0];

	if (dom_dropdown === null) {
		dom_dropdown = document.createElement("select");
		dom_dropdown.addEventListener("change", (event) => {
			dom_input.value = event.target.value;
		});
		dom_input.parentNode.insertBefore(dom_dropdown, dom_input);
	} else {
		dom_dropdown.innerHTML = "";
	}

	for (const [choice_key, choice_label, disabled] of choices) {
		const dom_option = document.createElement("option");
		dom_option.value = choice_key;
		dom_option.text = choice_label;
		dom_option.disabled = disabled;
		dom_option.selected = selection === undefined ? false : choice_key === selection;
		dom_dropdown.appendChild(dom_option);
	}

	return dom_dropdown;
}

class BEBBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {
	render(placeholder, prefix, initialState, initialError) {
		const block = super.render(placeholder, prefix, initialState, initialError);

		const dom_beb = block.container[0];
		const dom_field_block_container = dom_beb.closest(".formbuilder-field-block").parentNode
			.parentNode.parentNode;

		const fields = get_fields();
		const field_index =
			fields[dom_field_block_container.getAttribute("data-contentpath")].index;

		if (field_index === 0) {
			return block;
		}

		const dom_rules = build_virtual_dropdown(
			dom_beb.querySelector(".formbuilder-beb-field input"),
			get_field_choices(fields, field_index),
		);
		dom_rules.addEventListener("change", (event) => on_rule_subject_selected(event.target));
		on_rule_subject_selected(dom_rules);

		return block;
	}
}
window.telepath.register("forms.blocks.BooleanExpressionBuilderBlock", BEBBlockDefinition);
