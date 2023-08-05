from flask_boiler.context import Context as CTX

from google.cloud.firestore import Watch, DocumentSnapshot, \
    DocumentReference, Query

from flask_boiler.view_mediator import ViewMediatorBase


class ViewMediatorDAV(ViewMediatorBase):
    """
    Watches and updates Firestore for DocumentAsView view models
    """

    def __init__(self,
                 view_model_cls=None,
                 mutation_cls=None):
        """ Initializes a Document View Mediator.

        :param view_model_cls: the view model to be exposed with Document.
        :param mutation_cls: a subclass of Mutation to handle the changes
                made to the list of view models or a single view model.
        """
        super().__init__()
        self.view_model_cls = view_model_cls
        self.mutation_cls = mutation_cls
        self.rule_view_cls_mapping = dict()
        if self.view_model_cls is not None:
            self.default_tag = self.view_model_cls.__name__
        else:
            # Add default_tag as HIDDEN for internal hooks
            self.default_tag = "HIDDEN"
        self.instances = dict()

    @classmethod
    def notify(cls, obj):
        """
        Specifies what to do with the view model newly generated from an update.

        :param obj:
        :return:
        """
        obj.save()

    def _get_collection_name(self):
        return self.view_model_cls.__name__

    def _get_patch_query(self) -> Query:
        collection_group_id = "_PATCH_{}" \
            .format(self._get_collection_name())
        collection_group_query = CTX.db.collection_group(collection_group_id)
        return collection_group_query

    def _listen_to_patch(self):
        # NOTE: index for subcollection group may need to be created
        #   See: https://firebase.google.com/docs/firestore/query-data/queries#top_of_page

        def on_snapshot(snapshots, changes, timestamp):
            for doc in snapshots:
                # doc: DocumentSnapshot = snapshots[0]
                data = doc.to_dict()
                data = {
                    self.view_model_cls.get_schema_cls().g(key): val
                    for key, val in data.items()
                }

                # ie. doc from /UserViewDAV/user_id_a/_PATCH_UserViewDAV/patch_id_1
                parent_view_ref: DocumentReference = doc.reference.parent.parent
                obj = self.instances[parent_view_ref._document_path]

                self.mutation_cls.mutate_patch_one(obj=obj, data=data)

        watch = Watch.for_query(
            query=self._get_patch_query(),
            snapshot_callback=on_snapshot,
            snapshot_class_instance=DocumentSnapshot,
            reference_class_instance=DocumentReference)

    def start(self):
        """ Generates view models and listen to changes proposed to
                the view model.
        """
        self.instances = self.generate_entries()
        # time.sleep(3)  # TODO: delete after implementing sync
        self._listen_to_patch()

    def generate_entries(self):
        raise NotImplementedError


class ViewMediatorDeltaDAV(ViewMediatorBase):

    def notify(self, obj):
        """ Called when the object has state changes to be notified.

        :param obj: the object with state change
        :return:
        """
        obj.save()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "Protocol"):
            raise NotImplementedError

    def __init__(self, *args, query, **kwargs):
        """ Initializes a ViewMediator to declare protocols that
                are called when the results of a query change. Note that
                mediator.start must be called later.

        :param args:
        :param query: a listener will be attached to this query
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.query = query

    def _get_on_snapshot(self):
        """
        Implement in subclass
        :return:
        """
        def on_snapshot(snapshots, changes, timestamp):
            """
            Note that server reboot will result in some "Modified" objects
                to be routed as "Added" objects

            :param snapshots:
            :param changes:
            :param timestamp:
            :return:
            """
            for change in changes:
                snapshot = change.document
                assert isinstance(snapshot, DocumentSnapshot)
                try:
                    if change.type.name == 'ADDED':
                        self.Protocol.on_create(
                            snapshot=snapshot,
                            mediator=self
                        )
                    elif change.type.name == 'MODIFIED':
                        self.Protocol.on_update(
                            snapshot=snapshot,
                            mediator=self
                        )
                    elif change.type.name == 'REMOVED':
                        self.Protocol.on_delete(
                            snapshot=snapshot,
                            mediator=self
                        )
                except Exception as e:
                    """
                    Expects e to be printed to the logger 
                    """
                    CTX.logger.exception(f"DAV failed "
                                         f"for {snapshot.reference.path}")
                else:
                    CTX.logger.info(f"DAV succeeded "
                                    f"for {snapshot.reference.path}")

        return on_snapshot

    def start(self):
        """ Starts a listener to the query.

        :return:
        """

        query, on_snapshot = self.query, self._get_on_snapshot()

        watch = Watch.for_query(
            query=query,
            snapshot_callback=on_snapshot,
            snapshot_class_instance=DocumentSnapshot,
            reference_class_instance=DocumentReference
        )


class ProtocolBase:
    """ Protocol to specify actions when a document is 'ADDED', 'MODIFIED', and
            'REMOVED'.
    """

    @staticmethod
    def on_create(snapshot: DocumentSnapshot, mediator: ViewMediatorBase):
        """
        Called when a document is 'ADDED' to the result of a query

        :param snapshot:
        :param mediator:
        :return:
        """
        pass

    @staticmethod
    def on_update(snapshot: DocumentSnapshot, mediator: ViewMediatorBase):
        """
        Called when a document is 'MODIFIED' in the result of a query

        :param snapshot:
        :param mediator:
        :return:
        """
        pass

    @staticmethod
    def on_delete(snapshot: DocumentSnapshot, mediator: ViewMediatorBase):
        """
        Called when a document is 'REMOVED' in the result of a query

        :param snapshot:
        :param mediator:
        :return:
        """
        pass


def create_mutation_protocol(mutation):

    class _MutationProtocol:

        @staticmethod
        def on_create(snapshot, mediator):
            mutation.mutate_create(
                doc_id=snapshot.reference.id,
                data=snapshot.to_dict()
            )

    return _MutationProtocol
