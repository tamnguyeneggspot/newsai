/**
 * Shared filter sidebar for index and article pages.
 * Chỉ có bộ lọc Danh mục.
 * - renderFilterSidebar(containerId) — render HTML vào container
 * - loadFilterOptions(initialState) — load categories từ API và set giá trị
 * - getFilterState() — đọc category hiện tại từ DOM
 */

const FILTER_SELECT_CLASS = 'w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent';

function renderFilterSidebar(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = `
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-4 sticky top-24">
            <h3 class="text-sm font-semibold text-gray-700 mb-4">Bộ lọc</h3>
            <div class="space-y-4">
                <div>
                    <label class="block text-xs font-medium text-gray-500 mb-1.5">Danh mục</label>
                    <select id="categoryFilter" class="${FILTER_SELECT_CLASS}">
                        <option value="">Tất cả danh mục</option>
                    </select>
                </div>
            </div>
        </div>
    `;
}

async function generateFilterOption(selectEl, apiUrl, defaultLabel, currentValue) {
    if (!selectEl) return;
    const response = await fetch(apiUrl);
    const items = await response.json();
    selectEl.innerHTML = `<option value="">${defaultLabel}</option>`;
    items.forEach(item => {
        const option = document.createElement('option');
        option.value = item.name;
        option.textContent = `${item.name} (${item.count})`;
        selectEl.appendChild(option);
    });
    if (currentValue) selectEl.value = currentValue;
}

async function loadFilterOptions(initialState) {
    const state = initialState || {};
    const categoryFilter = document.getElementById('categoryFilter');
    if (categoryFilter) {
        await generateFilterOption(categoryFilter, '/api/categories', 'Tất cả danh mục', state.category);
    }
}

function getFilterState() {
    const categoryFilter = document.getElementById('categoryFilter');
    return {
        category: categoryFilter ? categoryFilter.value : ''
    };
}
