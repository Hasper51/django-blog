def test_get_post_list_pagination(mocker):
    mock_service = mocker.Mock(spec=BasePostService)
    mock_service.get_post_list.return_value = [mocker.Mock() for _ in range(5)]
    mock_service.get_post_count.return_value = 5

    mocker.patch('core.api.v1.posts.handlers.ORMPostService', return_value=mock_service)

    request = mocker.Mock(spec=HttpRequest)
    response = get_post_list(request)

    assert isinstance(response, ApiResponce)
    assert isinstance(response.data, ListPaginatedResponce)
    assert len(response.data.items) == 5
    assert response.data.pagination.offset == 0
    assert response.data.pagination.limit == 5
    assert response.data.pagination.total == 5

    mock_service.get_post_list.assert_called_once()
    mock_service.get_post_count.assert_called_once()