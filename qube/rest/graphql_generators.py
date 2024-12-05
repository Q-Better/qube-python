class BaseGraphQLGenerator:
    lookup_field = None
    query_structure = """
                        query {
                            %s %s {
                                pageInfo { startCursor endCursor hasNextPage hasPreviousPage }
                                edges {
                                    cursor
                                    node { 
                                        id
                                        %s
                                    }
                                }
                            }
                        }"""

    @classmethod
    def generate_query_filters(cls, **kwargs):
        filter_elements = [f'{k}:{v}' for k, v in kwargs.items()]
        filter_body = ','.join(filter_elements)
        return f"({filter_body})"

    @classmethod
    def generate_query_body(cls, **kwargs):
        query_filter = cls.generate_query_filters(**kwargs) if kwargs else ""
        return cls.query_structure % (cls.lookup_field, query_filter, "")


class QueuesListGraphQLGenerator(BaseGraphQLGenerator):
    lookup_field = "queues_lists_queues"
    queue_structure = """
                        queue {
                            id
                            tag
                            name
                            is_active
                            created_at
                            updated_at
                            deleted_at
                            allow_priority
                            ticket_range_enabled
                            min_ticket_number
                            max_ticket_number
                            ticket_tolerance_enabled
                            ticket_tolerance_number
                            kpi_wait_count
                            kpi_wait_time
                            kpi_service_time
                            location {
                                id
                            }
                            schedule {
                                    id
                            }
                        }"""

    @classmethod
    def generate_query_body(cls, **kwargs):
        query_filter = cls.generate_query_filters(**kwargs) if kwargs else ""
        return cls.query_structure % (cls.lookup_field, query_filter, cls.queue_structure)
