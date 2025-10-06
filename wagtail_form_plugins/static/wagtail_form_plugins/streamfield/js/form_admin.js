// https://jasonwatmore.com/vanilla-js-slugify-a-string-in-javascript
function slugify(input) {
	return !input
		? ""
		: input
				.toLowerCase()
				.trim()
				.normalize("NFD")
				.replace(/[\u0300-\u036f]/g, "")
				.replace(/[^a-z0-9\s-]/g, " ")
				.trim()
				.replace(/[\s-]+/g, "_");
}

function on_field_label_changed(dom_field_block) {
	const dom_field_label_input = dom_field_block.querySelector("[data-contentpath=label] input");
	const dom_field_slug_input = dom_field_block.querySelector("[data-contentpath=slug] input");
	if (dom_field_slug_input.value === "") {
		dom_field_slug_input.value = slugify(dom_field_label_input.value);
	}
}

class FormFieldBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {
	render(placeholder, prefix, initialState, initialError) {
		const block = super.render(placeholder, prefix, initialState, initialError);
		const dom_field_block = block.container[0];
		const dom_blocks_container =
			dom_field_block.parentElement.parentElement.parentElement.parentElement;
		const dom_inputs = dom_blocks_container.querySelectorAll(
			".formbuilder-field-block [data-contentpath=slug] input",
		);

		const prefixes = {};
		for (const dom_input of dom_inputs) {
			let prefix = dom_input.value.split("_").slice(0, -1).join("_");
			const counter = parseInt(dom_input.value.split("_").slice(-1).join(""));
			prefix = Number.isNaN(counter) ? dom_input.value : prefix;

			if (prefix in prefixes) {
				prefixes[prefix] += 1;
				dom_input.value = `${prefix}_${prefixes[prefix]}`;
			} else {
				prefixes[prefix] = 1;
			}
		}

		const dom_field_label = dom_field_block.querySelector("[data-contentpath=label]");
		dom_field_label.addEventListener("change", () => on_field_label_changed(dom_field_block));
		return block;
	}
}
window.telepath.register("forms.blocks.FormFieldBlock", FormFieldBlockDefinition);
