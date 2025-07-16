
function renderPagination(fnCaller, currentPage, totalPages, pageSize, pageGroup, pageContainerId = 'pagination') {
    // 기존 페이지네이션 초기화
    if(pageContainerId) {
        const pageContainer = $('#' + pageContainerId);
        pageContainer.empty();

    }

    // 한 그룹의 시작 · 끝 페이지 계산
    const startPage = Math.floor((currentPage - 1) / pageGroup) * pageGroup + 1;
    let endPage    = Math.min(startPage + pageGroup - 1, totalPages);
    const lastPage = Math.ceil(totalPages / pageSize);

    if (endPage >= lastPage) {
      endPage = lastPage;
    }

     // 처음 페이지로 이동 (<<)
    if (currentPage > 1) {
      pageContainer.append(`
        <li class="page-item">
            <a class="page-link" href="#" data-page=1>
                &laquo;
            </a>
        </li>
    `);
    }

    // "이전" 그룹 버튼 (<)
    if (currentPage > 1) {
      pageContainer.append(`
        <li class="page-item">
            <a class="page-link" href="#" data-page=${currentPage - 1}>
                &lsaquo;
            </a>
        </li>
    `);
    }

    // 페이지 번호 버튼
    for (let i = startPage; i <= endPage; i++) {
      pageContainer.append(`
            <li class="page-item ${i === currentPage ? 'active' : ''}">
                <a class="page-link" href="#" data-page=${i}>${i}</a>
            </li>
        `);
    }

    // "다음" 그룹 버튼 (>)
    if (currentPage < lastPage) {
      pageContainer.append(`
        <li class="page-item">
            <a class="page-link" href="#" data-page=${currentPage + 1}>
                &rsaquo;
            </a>
        </li>
    `);
    }

    // 마지막 페이지로 이동 (>>)
    if (currentPage < lastPage) {
      pageContainer.append(`
        <li class="page-item">
            <a class="page-link" href="#" data-page=${lastPage}>
                &raquo;
            </a>
        </li>
    `);
    }

    pageContainer.find("a.page-link").on('click', function () {
      let page = $(this).data("page");
      fnCaller(page);
    });

}
