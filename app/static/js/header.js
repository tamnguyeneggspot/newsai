/**
 * Shared header + mobile search for index and article pages.
 * Call renderHeader(options) after the script loads; options read from data attributes if not passed.
 *
 * @param {{ linkLogo?: boolean, showStats?: boolean }} [options]
 *   - linkLogo: wrap logo in <a href="/"> (true on article page)
 *   - showStats: show "Bài viết" / "Đã dịch" in header (true on article, false on index)
 */
function renderHeader(options) {
    const opts = options || {};
    const linkLogo = opts.linkLogo !== undefined ? opts.linkLogo : (document.body.dataset.headerLinkLogo === 'true');
    const showStats = opts.showStats !== undefined ? opts.showStats : (document.body.dataset.headerShowStats === 'true');

    const logoHtml = `
        <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/>
            </svg>
        </div>
        <div>
            <h1 class="text-xl font-bold text-gray-900">News AI</h1>
            <p class="text-xs text-gray-500">Tin tức thông minh</p>
        </div>`;

    const logoBlock = linkLogo
        ? '<a href="/" class="flex items-center space-x-3">' + logoHtml + '</a>'
        : '<div class="flex items-center space-x-3">' + logoHtml + '</div>';

    const headerHtml = `
    <header class="bg-white shadow-sm border-b border-gray-100 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <div class="flex items-center space-x-3">
                    ${logoBlock}
                </div>
                <div class="hidden md:flex flex-1 max-w-lg mx-8">
                    <div class="relative w-full">
                        <input type="text" id="searchInput"
                            class="w-full pl-10 pr-4 py-2.5 bg-gray-100 border-0 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all"
                            placeholder="Tìm kiếm tin tức...">
                        <svg class="absolute left-3 top-3 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                        </svg>
                    </div>
                </div>
                
            </div>
        </div>
    </header>
    <div class="md:hidden px-4 py-3 bg-white border-b">
        <div class="relative">
            <input type="text" id="searchInputMobile"
                class="w-full pl-10 pr-4 py-2.5 bg-gray-100 border-0 rounded-xl text-sm focus:ring-2 focus:ring-blue-500"
                placeholder="Tìm kiếm tin tức...">
            <svg class="absolute left-3 top-3 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
        </div>
    </div>`;

    const container = document.getElementById('header-container');
    if (container) container.innerHTML = headerHtml;
}
