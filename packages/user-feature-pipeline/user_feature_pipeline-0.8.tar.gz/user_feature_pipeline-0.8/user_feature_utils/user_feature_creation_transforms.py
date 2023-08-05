from apache_beam.utils.timestamp import MIN_TIMESTAMP
from apache_beam.utils.windowed_value import WindowedValue
from apache_beam.transforms.window import GlobalWindow
from apache_beam.transforms import PTransform, ParDo, DoFn
import google.cloud.storage as storage
import pandas as pd
import pickle


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


def download_blob(bucket_name, source_file, destination_file):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_file)
    result = blob.download_as_string(destination_file)
    return result


class _BatchingFn(DoFn):

    def __init__(self, batch_size=500):
        super(_BatchingFn, self).__init__()
        self._batch_size = batch_size

    def start_bundle(self):
        # buffer for string of lines
        self._lines = []

    def process(self, element):
        # Input element is anything (example a mongodb document)
        self._lines.append(element)
        if len(self._lines) >= self._batch_size:
            yield WindowedValue(self._lines, MIN_TIMESTAMP, [GlobalWindow()])
            self._flush_batch()

    def finish_bundle(self):
        # takes care of the unflushed buffer before finishing
        if self._lines:
            yield WindowedValue(self._lines, MIN_TIMESTAMP, [GlobalWindow()])
            self._flush_batch()

    def _flush_batch(self):
        self._lines = []


class BatchingFn(PTransform):

    def __init__(self, batch_size=500):
        super(BatchingFn, self).__init__()
        self._batch_size = batch_size

    def expand(self, pcoll):
        return pcoll | ParDo(_BatchingFn(self._batch_size))


class _CreateCategoricalEncodedVariables(DoFn):


    def process(self, data):
        # Multi Label Binarizer Variables
        # Split out Equipment Types

        equipment_mlb = pickle.load(download_blob("user_transforms", "user_equipment_mlb.pkl", "user_equipment_mlb.pkl"))
        state_lbe = pickle.load(download_blob("user_transforms", "user_state_lbe.pkl", "user_state_lbe.pkl"))
        state_ohe = pickle.load(download_blob("user_transforms", "user_state_ohe.pkl", "user_state_ohe.pkl"))
        city_lbe = pickle.load(download_blob("user_transforms", "user_city_lbe.pkl", "user_city_lbe.pkl"))
        city_ohe = pickle.load(download_blob("user_transforms", "user_city_ohe.pkl", "user_city_ohe.pkl"))
        email_lbe = pickle.load(download_blob("user_transforms", "user_email_lbe.pkl", "user_email_lbe.pkl"))
        email_ohe = pickle.load(download_blob("user_transforms", "user_email_ohe.pkl", "user_email_ohe.pkl"))
        zip_code_lbe = pickle.load(download_blob("user_transforms", "user_zip_code_lbe.pkl", "user_zip_code_lbe.pkl"))
        zip_code_ohe = pickle.load(download_blob("user_transforms", "user_zip_code_ohe.pkl", "user_zip_code_ohe.pkl"))
        channel_lbe = pickle.load(download_blob("user_transforms", "user_channel_lbe.pkl", "user_channel_lbe.pkl"))
        channel_ohe = pickle.load(download_blob("user_transforms", "user_channel_ohe.pkl", "user_channel_ohe.pkl"))
        dot_lbe = pickle.load(download_blob("user_transforms", "user_dot_lbe.pkl", "user_dot_lbe.pkl"))
        dot_ohe = pickle.load(download_blob("user_transforms", "user_dot_ohe.pkl", "user_dot_ohe.pkl"))
        hos_home_timezone_lbe = pickle.load(
            download_blob("user_transforms", "user_hos_home_timezone_lbe.pkl", "user_hos_home_timezone_lbe.pkl"))
        hos_home_timezone_ohe = pickle.load(
            download_blob("user_transforms", "user_hos_home_timezone_ohe.pkl", "user_hos_home_timezone_ohe.pkl"))
        hos_cycle_lbe = pickle.load(
            download_blob("user_transforms", "user_hos_cycle_lbe.pkl", "user_hos_cycle_lbe.pkl"))
        hos_cycle_ohe = pickle.load(
            download_blob("user_transforms", "user_hos_cycle_ohe.pkl", "user_hos_cycle_ohe.pkl"))
        mc_number_lbe = pickle.load(
            download_blob("user_transforms", "user_mc_number_lbe.pkl", "user_mc_number_lbe.pkl"))
        mc_number_ohe = pickle.load(
            download_blob("user_transforms", "user_mc_number_ohe.pkl", "user_mc_number_ohe.pkl"))
        user_type_lbe = pickle.load(
            download_blob("user_transforms", "user_user_type_lbe.pkl", "user_user_type_lbe.pkl"))
        user_type_ohe = pickle.load(
            download_blob("user_transforms", "user_user_type_ohe.pkl", "user_user_type_ohe.pkl"))
        safety_rating_lbe = pickle.load(
            download_blob("user_transforms", "user_safety_rating_lbe.pkl", "user_safety_rating_lbe.pkl"))
        safety_rating_ohe = pickle.load(
            download_blob("user_transforms", "user_safety_rating_ohe.pkl", "user_safety_rating_ohe.pkl"))

        df = pd.DataFrame(data)
        df.equipment_types.fillna(value=u'', inplace=True)
        df["equipment_types"] = df["equipment_types"].str.split(pat=", ")
        df["equipment_types_encoded"] = list(equipment_mlb.transform(df["equipment_types"]))
        df.drop("equipment_types", axis=1, inplace=True)

        # Split out Predicted Equipment Types
        df.predicted_equipment_types.fillna(value=u'', inplace=True)
        df["predicted_equipment_types"] = df["predicted_equipment_types"].str.split(pat=", ")
        df["predicted_equipment_types_encoded"] = list(equipment_mlb.transform(df["predicted_equipment_types"]))
        df.drop("predicted_equipment_types", axis=1, inplace=True)

        # One Hot Encode Variables
        # State
        state_encoded = state_lbe.transform(df['state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["state_encoded"] = list(data)
        df.drop("state", axis=1, inplace=True)

        # City
        city_encoded = city_lbe.transform(df['city'])
        df["city_encoded"] = list(city_ohe.transform(city_encoded.reshape(-1, 1)))
        df.drop("city", axis=1, inplace=True)

        # Zip Code
        zip_code_encoded = zip_code_lbe.transform(df['zip_code'])
        df["zip_code_encoded"] = list(zip_code_ohe.transform(zip_code_encoded.reshape(-1, 1)))
        df.drop("zip_code", axis=1, inplace=True)

        # Email
        email_encoded = email_lbe.transform(df['email'])
        df["email_encoded"] = list(email_ohe.transform(email_encoded.reshape(-1, 1)))
        df.drop("email", axis=1, inplace=True)

        # DOT
        dot_encoded = dot_lbe.transform(df['dot'])
        df["dot_encoded"] = list(dot_ohe.transform(dot_encoded.reshape(-1, 1)))
        df.drop("dot", axis=1, inplace=True)

        # Channel
        channel_encoded = channel_lbe.transform(df['channel'])
        df["channel_encoded"] = list(channel_ohe.transform(channel_encoded.reshape(-1, 1)))
        df.drop("channel", axis=1, inplace=True)

        # hos_cycle
        hos_cycle_encoded = hos_cycle_lbe.transform(df['hos_cycle'])
        df["hos_cycle_encoded"] = list(hos_cycle_ohe.transform(hos_cycle_encoded.reshape(-1, 1)))
        df.drop("hos_cycle", axis=1, inplace=True)

        # hos_home_timezone
        hos_home_timezone_encoded = hos_home_timezone_lbe.transform(df['hos_home_timezone'])
        df["hos_home_timezone_encoded"] = list(
            hos_home_timezone_ohe.transform(hos_home_timezone_encoded.reshape(-1, 1)))
        df.drop("hos_home_timezone", axis=1, inplace=True)

        # mc_number
        mc_number_encoded = mc_number_lbe.transform(df['mc_number'])
        df["mc_number_encoded"] = list(mc_number_ohe.transform(mc_number_encoded.reshape(-1, 1)))
        df.drop("mc_number", axis=1, inplace=True)

        # user_type
        user_type_encoded = user_type_lbe.transform(df['user_type'])
        df["user_type_encoded"] = list(user_type_ohe.transform(user_type_encoded.reshape(-1, 1)))
        df.drop("user_type", axis=1, inplace=True)

        # Operating Lanes Pickup States
        state_encoded = state_lbe.transform(df['operating_lanes_1_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_1_pickup_state_encoded"] = list(data)
        df.drop("operating_lanes_1_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_2_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_2_pickup_state_encoded"] = list(data)
        df.drop("operating_lanes_2_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_3_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_3_pickup_state_encoded"] = list(data)
        df.drop("operating_lanes_3_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_4_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_4_pickup_state_encoded"] = list(data)
        df.drop("operating_lanes_4_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_5_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_5_pickup_state_encoded"] = list(data)
        df.drop("operating_lanes_5_pickup_state", axis=1, inplace=True)

        # Operating Lanes Dropoff States
        state_encoded = state_lbe.transform(df['operating_lanes_1_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_1_dropoff_state_encoded"] = list(data)
        df.drop("operating_lanes_1_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_2_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_2_dropoff_state_encoded"] = list(data)
        df.drop("operating_lanes_2_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_3_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_3_dropoff_state_encoded"] = list(data)
        df.drop("operating_lanes_3_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_4_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_4_dropoff_state_encoded"] = list(data)
        df.drop("operating_lanes_4_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['operating_lanes_5_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["operating_lanes_5_dropoff_state_encoded"] = list(data)
        df.drop("operating_lanes_5_dropoff_state", axis=1, inplace=True)

        # Operating Lanes Pickup Cities
        city_encoded = city_lbe.transform(df['operating_lanes_1_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_1_pickup_city_encoded"] = list(data)
        df.drop("operating_lanes_1_pickup_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_2_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_2_pickup_city_encoded"] = list(data)
        df.drop("operating_lanes_2_pickup_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_3_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_3_pickup_city_encoded"] = list(data)
        df.drop("operating_lanes_3_pickup_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_4_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_4_pickup_city_encoded"] = list(data)
        df.drop("operating_lanes_4_pickup_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_5_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_5_pickup_city_encoded"] = list(data)
        df.drop("operating_lanes_5_pickup_city", axis=1, inplace=True)

        # Operating Lanes Dropoff Cities
        city_encoded = city_lbe.transform(df['operating_lanes_1_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_1_dropoff_city_encoded"] = list(data)
        df.drop("operating_lanes_1_dropoff_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_2_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_2_dropoff_city_encoded"] = list(data)
        df.drop("operating_lanes_2_dropoff_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_3_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_3_dropoff_city_encoded"] = list(data)
        df.drop("operating_lanes_3_dropoff_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_4_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_4_dropoff_city_encoded"] = list(data)
        df.drop("operating_lanes_4_dropoff_city", axis=1, inplace=True)

        city_encoded = city_lbe.transform(df['operating_lanes_5_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["operating_lanes_5_dropoff_city_encoded"] = list(data)
        df.drop("operating_lanes_5_dropoff_city", axis=1, inplace=True)

        # Common Lanes Pickup States
        state_encoded = state_lbe.transform(df['common_lane_1_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_1_pickup_state_encoded"] = list(data)
        df.drop("common_lane_1_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_2_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_2_pickup_state_encoded"] = list(data)
        df.drop("common_lane_2_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_3_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_3_pickup_state_encoded"] = list(data)
        df.drop("common_lane_3_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_4_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_4_pickup_state_encoded"] = list(data)
        df.drop("common_lane_4_pickup_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_5_pickup_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_5_pickup_state_encoded"] = list(data)
        df.drop("common_lane_5_pickup_state", axis=1, inplace=True)

        # Common Lanes Dropoff States
        state_encoded = state_lbe.transform(df['common_lane_1_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_1_dropoff_state_encoded"] = list(data)
        df.drop("common_lane_1_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_2_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_2_dropoff_state_encoded"] = list(data)
        df.drop("common_lane_2_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_3_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_3_dropoff_state_encoded"] = list(data)
        df.drop("common_lane_3_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_4_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_4_dropoff_state_encoded"] = list(data)
        df.drop("common_lane_4_dropoff_state", axis=1, inplace=True)

        state_encoded = state_lbe.transform(df['common_lane_5_dropoff_state'])
        data = state_ohe.transform(state_encoded.reshape(-1, 1))
        df["common_lane_5_dropoff_state_encoded"] = list(data)
        df.drop("common_lane_5_dropoff_state", axis=1, inplace=True)

        # Common Lanes Pickup Cities
        df.loc[~df["common_lane_1_pickup_city"].isin(city_lbe.classes_), "common_lane_1_pickup_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_1_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_1_pickup_city_encoded"] = list(data)
        df.drop("common_lane_1_pickup_city", axis=1, inplace=True)

        df.loc[~df["common_lane_2_pickup_city"].isin(city_lbe.classes_), "common_lane_2_pickup_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_2_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_2_pickup_city_encoded"] = list(data)
        df.drop("common_lane_2_pickup_city", axis=1, inplace=True)

        df.loc[~df["common_lane_3_pickup_city"].isin(city_lbe.classes_), "common_lane_3_pickup_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_3_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_3_pickup_city_encoded"] = list(data)
        df.drop("common_lane_3_pickup_city", axis=1, inplace=True)

        df.loc[~df["common_lane_4_pickup_city"].isin(city_lbe.classes_), "common_lane_4_pickup_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_4_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_4_pickup_city_encoded"] = list(data)
        df.drop("common_lane_4_pickup_city", axis=1, inplace=True)

        df.loc[~df["common_lane_5_pickup_city"].isin(city_lbe.classes_), "common_lane_5_pickup_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_5_pickup_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_5_pickup_city_encoded"] = list(data)
        df.drop("common_lane_5_pickup_city", axis=1, inplace=True)

        # Common Lanes Dropoff Cities
        df.loc[~df["common_lane_1_dropoff_city"].isin(city_lbe.classes_), "common_lane_1_dropoff_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_1_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_1_dropoff_city_encoded"] = list(data)
        df.drop("common_lane_1_dropoff_city", axis=1, inplace=True)

        df.loc[~df["common_lane_2_dropoff_city"].isin(city_lbe.classes_), "common_lane_2_dropoff_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_2_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_2_dropoff_city_encoded"] = list(data)
        df.drop("common_lane_2_dropoff_city", axis=1, inplace=True)

        df.loc[~df["common_lane_3_dropoff_city"].isin(city_lbe.classes_), "common_lane_3_dropoff_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_3_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_3_dropoff_city_encoded"] = list(data)
        df.drop("common_lane_3_dropoff_city", axis=1, inplace=True)

        df.loc[~df["common_lane_4_dropoff_city"].isin(city_lbe.classes_), "common_lane_4_dropoff_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_4_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_4_dropoff_city_encoded"] = list(data)
        df.drop("common_lane_4_dropoff_city", axis=1, inplace=True)

        df.loc[~df["common_lane_5_dropoff_city"].isin(city_lbe.classes_), "common_lane_5_dropoff_city"] = None
        city_encoded = city_lbe.transform(df['common_lane_5_dropoff_city'])
        data = city_ohe.transform(city_encoded.reshape(-1, 1))
        df["common_lane_5_dropoff_city_encoded"] = list(data)
        df.drop("common_lane_5_dropoff_city", axis=1, inplace=True)

        safety_rating_encoded = safety_rating_lbe.transform(df['safer_result_safety_rating'])
        df["safer_result_safety_rating_encoded"] = list(safety_rating_ohe.transform(safety_rating_encoded.reshape(-1, 1)))
        df.drop("safer_result_safety_rating", axis=1, inplace=True)

        return [df, ]


class CreateCategoricalEncodedVariables(PTransform):

    def expand(self, pcoll):
        return pcoll | ParDo(_CreateCategoricalEncodedVariables())


class _SaveDataframeToGCS(DoFn):

    def process(self, df):
        bundle_num = df.iloc[0]["person_id"]
        filename = "user_features_" + str(bundle_num) + ".pkl"
        df.to_pickle(filename)
        upload_blob("user_features", filename, filename)

        return [df, ]


class SaveDataframeToGCS(PTransform):

    def expand(self, pcoll):
        return pcoll | ParDo(_SaveDataframeToGCS())